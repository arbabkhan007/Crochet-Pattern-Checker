"""Web pattern import with an SSRF guard.

Fetching a user-supplied URL from the server is a classic SSRF sink, so this
module resolves the host, refuses private and link-local targets, bounds
redirects, bytes and time, and accepts only text-ish content types.

The result is plain text handed to the existing parser. Nothing here parses,
counts or validates a pattern: ``crochet_checker`` still owns that, and a page
that yields no instructions simply yields no instructions.
"""

from __future__ import annotations

import ipaddress
import re
import socket
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import urljoin, urlparse

import httpx

MAX_BYTES = 3 * 1024 * 1024
TIMEOUT_SECONDS = 12.0
MAX_REDIRECTS = 3
ALLOWED_TYPES = (
    "text/html",
    "text/plain",
    "application/xhtml+xml",
    "text/markdown",
)

# Element class/id names that mark promotional or navigational blocks.
_BLOCK_PATTERN = re.compile(
    r"""(?:^|[\s"'])(?:ad|ads|advert\w*|adsbygoogle|promo\w*|banner|sidebar|"""
    r"""share\w*|related\w*|newsletter|cookie\w*|comment\w*)(?:[\s"']|$)""",
    re.IGNORECASE,
)

_DROP_ELEMENTS = re.compile(
    r"<(script|style|noscript|svg|iframe|form|nav|footer|header)\b[\s\S]*?</\1>",
    re.IGNORECASE,
)
_COMMENTS = re.compile(r"<!--[\s\S]*?-->")
_BLOCK_ELEMENTS = re.compile(
    r"<(div|aside|section|ul|span)\b([^>]*)>([\s\S]*?)</\1>",
    re.IGNORECASE,
)
_BREAKS = re.compile(r"<br\s*/?>", re.IGNORECASE)
_BLOCK_ENDS = re.compile(
    r"</(p|div|li|h[1-6]|tr|section|article|blockquote)>", re.IGNORECASE
)
_LIST_ITEMS = re.compile(r"<li[^>]*>", re.IGNORECASE)
_TAGS = re.compile(r"<[^>]+>")
_TITLE = re.compile(r"<title[^>]*>([\s\S]*?)</title>", re.IGNORECASE)

_ENTITIES = {
    "amp": "&",
    "lt": "<",
    "gt": ">",
    "quot": '"',
    "apos": "'",
    "nbsp": " ",
    "ndash": "-",
    "mdash": "-",
    "rsquo": "'",
    "lsquo": "'",
    "ldquo": '"',
    "rdquo": '"',
    "hellip": "...",
}


class ImportError_(ValueError):
    """A refusal or failure that is safe to show to the caller."""

    def __init__(self, message: str, status: int = 400) -> None:
        super().__init__(message)
        self.status = status


@dataclass(frozen=True)
class ImportedPage:
    url: str
    title: str
    text: str
    content_type: str
    truncated: bool


def _is_public(address: str) -> bool:
    try:
        parsed = ipaddress.ip_address(address)
    except ValueError:
        return False
    if (
        parsed.is_private
        or parsed.is_loopback
        or parsed.is_link_local
        or parsed.is_reserved
        or parsed.is_multicast
        or parsed.is_unspecified
    ):
        return False
    # IPv4-mapped IPv6 must be judged on the embedded address.
    if parsed.version == 6 and parsed.ipv4_mapped is not None:
        return _is_public(str(parsed.ipv4_mapped))
    return True


def _resolve(hostname: str) -> list[str]:
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as error:
        raise ImportError_(f"Could not resolve {hostname}.", status=502) from error
    return sorted({info[4][0] for info in infos})


def _assert_public_url(raw_url: str) -> str:
    parsed = urlparse(raw_url)
    if parsed.scheme not in ("http", "https"):
        raise ImportError_("Only http and https URLs can be imported.")
    hostname = parsed.hostname or ""
    if not hostname:
        raise ImportError_("That is not a valid URL.")
    lowered = hostname.lower()
    if lowered == "localhost" or lowered.endswith((".local", ".internal")):
        raise ImportError_("Local network addresses cannot be imported.")

    addresses = _resolve(hostname)
    if not addresses:
        raise ImportError_(f"Could not resolve {hostname}.", status=502)
    if not all(_is_public(address) for address in addresses):
        raise ImportError_("Private addresses cannot be imported.")
    return raw_url


def _decode_entities(text: str) -> str:
    def numeric(match: re.Match[str]) -> str:
        code = match.group(1)
        try:
            return chr(int(code, 16) if code.lower().startswith("x") else int(code))
        except (ValueError, OverflowError):
            return match.group(0)

    text = re.sub(r"&#(x?[0-9a-fA-F]+);", numeric, text)

    def named(match: re.Match[str]) -> str:
        return _ENTITIES.get(match.group(1).lower(), match.group(0))

    return re.sub(r"&([a-zA-Z]+);", named, text)


def _strip_block(match: re.Match[str]) -> str:
    return " " if _BLOCK_PATTERN.search(match.group(2) or "") else match.group(0)


def html_to_pattern_text(html: str) -> tuple[str, str]:
    """Return ``(title, text)`` with navigation and promotional blocks removed."""
    title_match = _TITLE.search(html)
    title = _decode_entities(title_match.group(1)).strip() if title_match else ""

    # Strip promotional blocks while their class/id attributes still exist.
    body = _BLOCK_ELEMENTS.sub(_strip_block, html)
    body = _DROP_ELEMENTS.sub(" ", body)
    body = _COMMENTS.sub(" ", body)
    body = _BREAKS.sub("\n", body)
    body = _BLOCK_ENDS.sub("\n", body)
    body = _LIST_ITEMS.sub("\u2022 ", body)
    body = _TAGS.sub(" ", body)
    body = _decode_entities(body)

    lines: list[str] = []
    for line in body.splitlines():
        cleaned = re.sub(r"[ \t\u00a0]+", " ", line).strip()
        if cleaned or (lines and lines[-1]):
            lines.append(cleaned)

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    return title, text


def _stream(response: httpx.Response) -> tuple[bytes, bool]:
    chunks: list[bytes] = []
    received = 0
    truncated = False
    for chunk in response.iter_bytes():
        received += len(chunk)
        if received > MAX_BYTES:
            truncated = True
            break
        chunks.append(chunk)
    return b"".join(chunks), truncated


def import_pattern_page(
    raw_url: str,
    *,
    transport: httpx.BaseTransport | None = None,
) -> ImportedPage:
    """Fetch a public page and reduce it to text. Raises ImportError_ on refusal.

    ``transport`` exists for tests: it lets the fetch, redirect and size limits be
    exercised without real network access. It must not be reachable from the API.
    """
    url = _assert_public_url(raw_url.strip())
    truncated = False

    with httpx.Client(
        transport=transport,
        timeout=TIMEOUT_SECONDS,
        follow_redirects=False,
        headers={
            "User-Agent": "CrochetPatternChecker/1.0 (pattern importer)",
            "Accept": "text/html,text/plain;q=0.9",
            "Accept-Language": "en",
        },
    ) as client:
        response: httpx.Response | None = None
        for _ in range(MAX_REDIRECTS + 1):
            try:
                response = client.get(url)
            except httpx.TimeoutException as error:
                raise ImportError_("The site took too long to respond.", status=504) from error
            except httpx.HTTPError as error:
                raise ImportError_("Could not reach that site.", status=502) from error

            if response.is_redirect:
                location = response.headers.get("location")
                if not location:
                    raise ImportError_("The site sent an invalid redirect.", status=502)
                url = _assert_public_url(urljoin(url, location))
                continue
            break

        if response is None:
            raise ImportError_("Could not reach that site.", status=502)
        if response.status_code >= 400:
            raise ImportError_(f"The site returned {response.status_code}.", status=502)

        content_type = (
            response.headers.get("content-type", "").split(";")[0].strip().lower()
        )
        if content_type not in ALLOWED_TYPES:
            raise ImportError_(
                "That link returns "
                f"{content_type or 'an unknown type'}. Try a page URL, or download "
                "the PDF and use the PDF tab.",
                status=415,
            )

        payload, truncated = _stream(response)

    text = payload.decode("utf-8", errors="replace")
    if content_type in ("text/plain", "text/markdown"):
        title = urlparse(url).path.rstrip("/").split("/")[-1] or urlparse(url).hostname or ""
        return ImportedPage(url, title, text.strip(), content_type, truncated)

    title, cleaned = html_to_pattern_text(text)
    return ImportedPage(
        url,
        title or urlparse(url).hostname or "",
        cleaned,
        content_type,
        truncated,
    )


def instruction_lines(text: str) -> Iterable[str]:
    """Lines that look like written instructions. Used only for reporting counts."""
    return (
        line
        for line in text.splitlines()
        if re.match(r"^\s*(?:row|rnd|round|r)\s*\d+", line, re.IGNORECASE)
    )
