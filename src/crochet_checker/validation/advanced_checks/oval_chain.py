"""Foundation-chain accounting for explicit oval top/return passes."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .common import AdvancedFinding, meaningful_lines


@dataclass(frozen=True)
class ChainWork:
    """Chains consumed and stitches produced by one pass operation."""

    chains_consumed: int
    stitches_produced: int


def validate_oval_foundation(
    ch_count: int,
    start_ch_from_hook: int,
    top_ops: list[ChainWork | tuple[int, int]],
    bottom_ops: list[ChainWork | tuple[int, int]],
) -> tuple[list[str], int]:
    """Validate one oval's two sides without confusing stitch production with chain use.

    A multi-stitch corner operation such as ``2 sc in 2nd ch`` consumes one
    foundation chain, not two. The top pass must cover every usable chain;
    the return pass may use no more than ``n_available - 1`` chains.
    """
    if ch_count < 1 or start_ch_from_hook < 1:
        raise ValueError("Chain count and starting-chain index must be positive.")
    if start_ch_from_hook > ch_count:
        raise ValueError(
            "Starting-chain index cannot exceed the foundation-chain length."
        )

    def totals(ops: list[ChainWork | tuple[int, int]]) -> tuple[int, int]:
        consumed = produced = 0
        for op in ops:
            c, s = (
                (op.chains_consumed, op.stitches_produced)
                if isinstance(op, ChainWork)
                else op
            )
            if c < 0 or s < 0:
                raise ValueError("Chain and stitch counts cannot be negative.")
            consumed += int(c)
            produced += int(s)
        return consumed, produced

    n_available = ch_count - (start_ch_from_hook - 1)
    top_chains, top_stitches = totals(top_ops)
    return_chains, return_stitches = totals(bottom_ops)
    errors: list[str] = []

    if top_chains != n_available:
        errors.append(
            f"Oval top pass consumes {top_chains} chains, but {n_available} "
            f"are available from a chain of {ch_count} starting in chain "
            f"{start_ch_from_hook}."
        )
    max_return = max(n_available - 1, 0)
    if return_chains > max_return:
        middle = max(n_available - 2, 0)
        errors.append(
            f"Oval return pass consumes {return_chains} chains, but only "
            f"{middle} middle chains plus at most one starting-end chain "
            f"({max_return} total) are available."
        )
    return errors, top_stitches + return_stitches


_ORDINAL_CHAIN = re.compile(
    r"(?:(\d+)(?:st|nd|rd|th)|first|last)\s+(?:foundation\s+)?(?:ch|chain)\b",
    re.IGNORECASE,
)
_START_FROM_HOOK = re.compile(
    r"(\d+)(?:st|nd|rd|th)\s+(?:foundation\s+)?(?:ch|chain)\s+from\s+(?:the\s+)?hook",
    re.IGNORECASE,
)
_CHAIN_COUNT = re.compile(r"\b(?:ch|chain|chains)\s*(?:of\s*)?(\d+)\b", re.IGNORECASE)
_RETURN_MARKER = re.compile(
    r"\b(?:on|along|working(?:\s+on)?|continue(?:d)?)\s+(?:the\s+)?(?:opposite|other)\s+side\b|\breturn\s+pass\b",
    re.IGNORECASE,
)
_STITCH_NAME = r"(?:sc|hdc|dc|tr|dtr)"
_CHAIN_OPS = re.compile(
    rf"(?:(?P<produced>\d+)\s+)?{_STITCH_NAME}\s+(?:in|into)\s+(?:the\s+)?"
    rf"(?P<endpoint>(?:\d+)(?:st|nd|rd|th)|first|last)\s+(?:foundation\s+)?(?:ch|chain)\b"
    rf"|(?:(?P<each>\d+)\s+)?{_STITCH_NAME}\s+(?:in|into)\s+(?:the\s+)?next\s+(?P<chains>\d+)\s+(?:foundation\s+)?(?:ch|chain)s?\b",
    re.IGNORECASE,
)


def _pass_ops(text: str) -> list[ChainWork]:
    result: list[ChainWork] = []
    for match in _CHAIN_OPS.finditer(text):
        if match.group("endpoint"):
            result.append(ChainWork(1, int(match.group("produced") or 1)))
        else:
            chains = int(match.group("chains"))
            multiplier = int(match.group("each") or 1)
            result.append(ChainWork(chains, chains * multiplier))
    return result


def oval_findings(text: str) -> list[AdvancedFinding]:
    """Read only self-contained oval instructions with explicit pass boundaries.

    If the foundation count, start index, or return-side marker is absent, this
    scanner stays silent rather than guessing how the chain is traversed.
    """
    findings: list[AdvancedFinding] = []
    for line_number, raw in meaningful_lines(text):
        if not re.search(r"\boval\b", raw, re.IGNORECASE):
            continue
        count_match = _CHAIN_COUNT.search(raw)
        start_match = _START_FROM_HOOK.search(raw)
        return_match = _RETURN_MARKER.search(raw)
        if not count_match or not start_match or not return_match:
            continue
        top_ops = _pass_ops(raw[: return_match.start()])
        return_ops = _pass_ops(raw[return_match.end() :])
        if not top_ops or not return_ops:
            continue
        try:
            errors, _total = validate_oval_foundation(
                int(count_match.group(1)),
                int(start_match.group(1)),
                top_ops,
                return_ops,
            )
        except ValueError as error:
            findings.append(
                AdvancedFinding(
                    "OvalFoundationAccounting",
                    f"The explicit oval foundation instruction is inconsistent: {error}",
                    "error",
                    line_number,
                )
            )
            continue
        findings.extend(
            AdvancedFinding("OvalFoundationAccounting", message, "error", line_number)
            for message in errors
        )
        if not errors:
            return_chains = sum(
                operation.chains_consumed
                if isinstance(operation, ChainWork)
                else operation[0]
                for operation in return_ops
            )
            available_return = max(
                int(count_match.group(1)) - int(start_match.group(1)),
                0,
            )
            if return_chains < available_return:
                findings.append(
                    AdvancedFinding(
                        "OvalReturnUnaccountedChains",
                        f"The explicit oval return-side operations consume {return_chains} of {available_return} remaining chains. Confirm that any skipped foundation chains are intentional.",
                        "warning",
                        line_number,
                    )
                )
    return findings
