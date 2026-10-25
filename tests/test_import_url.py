"""Tests for the web pattern importer and its SSRF guard.

The guard is the risky part of this module, so the refusal cases are tested
directly rather than through a live server.
"""

from __future__ import annotations

import pytest

from crochet_checker.web.import_url import (
    ImportError_,
    _assert_public_url,
    _is_public,
    html_to_pattern_text,
    instruction_lines,
)


@pytest.mark.parametrize(
    "address",
    [
        "127.0.0.1",
        "10.1.2.3",
        "172.16.0.1",
        "192.168.1.1",
        "169.254.169.254",  # cloud metadata
        "0.0.0.0",
        "::1",
        "fe80::1",
        "fc00::1",
        "::ffff:127.0.0.1",
    ],
)
def test_private_and_special_addresses_are_not_public(address: str) -> None:
    assert _is_public(address) is False


@pytest.mark.parametrize("address", ["93.184.216.34", "1.1.1.1", "2606:4700:4700::1111"])
def test_public_addresses_are_public(address: str) -> None:
    assert _is_public(address) is True


@pytest.mark.parametrize(
    "url",
    [
        "file:///etc/passwd",
        "ftp://example.com/pattern",
        "javascript:alert(1)",
        "not a url",
        "",
    ],
)
def test_non_http_schemes_are_refused(url: str) -> None:
    with pytest.raises(ImportError_):
        _assert_public_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "http://localhost/pattern",
        "http://127.0.0.1/pattern",
        "http://169.254.169.254/latest/meta-data/",
        "http://10.0.0.5/pattern",
        "http://printer.local/pattern",
        "http://metadata.internal/pattern",
    ],
)
def test_local_and_private_hosts_are_refused(url: str) -> None:
    with pytest.raises(ImportError_):
        _assert_public_url(url)


def test_html_keeps_instructions_and_drops_furniture() -> None:
    html = """
    <html><head><title>Free Washcloth Pattern</title>
    <style>.ad{color:red}</style></head>
    <body>
      <nav>Home | Shop | Blog</nav>
      <script>tracking()</script>
      <h1>Simple Washcloth</h1>
      <p>Yarn: worsted cotton</p>
      <p>Row 1: ch 21, sc in 2nd ch from hook and in each ch across (20)</p>
      <div class="ad">BUY YARN NOW</div>
      <p>Row 2: ch 1, turn, sc in each st across (20)</p>
      <div id="sidebar">Related posts</div>
      <footer>&copy; 2026</footer>
    </body></html>
    """
    title, text = html_to_pattern_text(html)
    assert title == "Free Washcloth Pattern"
    assert "Row 1: ch 21" in text
    assert "Row 2: ch 1" in text
    assert "tracking()" not in text
    assert "BUY YARN NOW" not in text
    assert "Related posts" not in text
    assert "Home | Shop" not in text


def test_html_decodes_entities_so_counts_survive() -> None:
    _, text = html_to_pattern_text("<p>sc in each st &ndash; 20 sts&hellip;</p>")
    assert "20 sts" in text
    assert "\u2013" not in text  # ndash decoded


def test_instruction_lines_finds_labelled_rows_only() -> None:
    text = "Materials\nRow 1: ch 21 (20)\nnote: keep loose\nRound 2: sc around (20)"
    found = list(instruction_lines(text))
    assert len(found) == 2
    assert found[0].startswith("Row 1")
    assert found[1].startswith("Round 2")


def test_import_of_plain_text_url_shape() -> None:
    # A refusal must not leak a stack trace or a socket error message.
    with pytest.raises(ImportError_) as caught:
        _assert_public_url("http://127.0.0.1:8000/admin")
    assert "Private addresses" in str(caught.value) or "Local network" in str(caught.value)


# --- fetch, redirect and limit behaviour, without real network access -------

import httpx

from crochet_checker.web.import_url import MAX_BYTES, import_pattern_page

PUBLIC = "93.184.216.34"


def _handler_for(routes: dict[str, httpx.Response | tuple[int, dict[str, str]]]):
    def handler(request: httpx.Request) -> httpx.Response:
        key = str(request.url)
        reply = routes.get(key)
        if reply is None:
            return httpx.Response(404)
        if isinstance(reply, tuple):
            status, headers = reply
            return httpx.Response(status, headers=headers)
        return reply

    return handler


def test_import_extracts_pattern_text_from_html() -> None:
    html = (
        "<html><head><title>Sock Pattern</title></head><body>"
        "<nav>menu</nav><p>Row 1: ch 21 (20)</p></body></html>"
    )
    transport = httpx.MockTransport(
        _handler_for(
            {
                "http://example.com/p": httpx.Response(
                    200, text=html, headers={"content-type": "text/html"}
                )
            }
        )
    )
    page = import_pattern_page("http://example.com/p", transport=transport)
    assert page.title == "Sock Pattern"
    assert "Row 1: ch 21" in page.text
    assert "menu" not in page.text
    assert page.truncated is False


def test_import_rejects_non_text_content_type() -> None:
    transport = httpx.MockTransport(
        _handler_for(
            {
                "http://example.com/f.pdf": httpx.Response(
                    200, headers={"content-type": "application/pdf"}, content=b"%PDF-1.4"
                )
            }
        )
    )
    with pytest.raises(ImportError_) as caught:
        import_pattern_page("http://example.com/f.pdf", transport=transport)
    assert "PDF" in str(caught.value)
    assert caught.value.status == 415


def test_import_refuses_redirect_into_private_space() -> None:
    transport = httpx.MockTransport(
        _handler_for(
            {
                "http://example.com/go": (
                    302,
                    {"location": "http://127.0.0.1/secret"},
                )
            }
        )
    )
    with pytest.raises(ImportError_):
        import_pattern_page("http://example.com/go", transport=transport)


def test_import_follows_public_redirect() -> None:
    transport = httpx.MockTransport(
        _handler_for(
            {
                "http://example.com/a": (301, {"location": "http://example.com/b"}),
                "http://example.com/b": httpx.Response(
                    200,
                    text="<title>B</title><p>Round 1: 6 sc (6)</p>",
                    headers={"content-type": "text/html"},
                ),
            }
        )
    )
    page = import_pattern_page("http://example.com/a", transport=transport)
    assert page.title == "B"
    assert "Round 1" in page.text


def test_import_stops_after_too_many_redirects() -> None:
    loop = {"http://example.com/loop": (302, {"location": "http://example.com/loop"})}
    transport = httpx.MockTransport(_handler_for(loop))
    with pytest.raises(ImportError_):
        import_pattern_page("http://example.com/loop", transport=transport)


def test_import_reports_server_error_without_leaking_detail() -> None:
    transport = httpx.MockTransport(
        _handler_for({"http://example.com/x": httpx.Response(500, text="traceback stuff")})
    )
    with pytest.raises(ImportError_) as caught:
        import_pattern_page("http://example.com/x", transport=transport)
    assert "traceback" not in str(caught.value)
    assert "500" in str(caught.value)


def test_import_truncates_oversized_bodies() -> None:
    huge = "<p>" + ("sc in each st around " * ((MAX_BYTES // 20) + 1000)) + "</p>"
    transport = httpx.MockTransport(
        _handler_for(
            {
                "http://example.com/big": httpx.Response(
                    200, text=huge, headers={"content-type": "text/html"}
                )
            }
        )
    )
    page = import_pattern_page("http://example.com/big", transport=transport)
    assert page.truncated is True
    assert len(page.text) < len(huge)


def test_import_refuses_a_response_with_no_content_type() -> None:
    transport = httpx.MockTransport(
        _handler_for(
            {"http://example.com/raw": httpx.Response(200, content=b"<title>x</title>")}
        )
    )
    with pytest.raises(ImportError_) as caught:
        import_pattern_page("http://example.com/raw", transport=transport)
    assert caught.value.status == 415
