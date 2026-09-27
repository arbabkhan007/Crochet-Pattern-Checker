"""Assembly and fabric-density checks for the validation pipeline.

These read explicit pattern statements. They do not invent stitch counts,
and they do not change the existing stitch-math errors.
"""

from __future__ import annotations

import re


class AssemblyInterfaceValidator:
    """Enforce the 3-number assembly rule on an explicit socket join."""

    def validate_socket_join(
        self,
        prev_body_sts,
        worked_body_sts,
        skipped_body_sts,
        limb_held_sts,
    ):
        errors = []
        previous = int(prev_body_sts)
        worked = int(worked_body_sts)
        skipped = int(skipped_body_sts)
        held = int(limb_held_sts)
        consumed = worked + skipped
        if consumed != previous:
            errors.append(
                f"Body Stitch Drop: Expected {previous} total body sts, "
                f"but worked ({worked}) + skipped ({skipped}) = {consumed}."
            )
        if held != skipped:
            errors.append(
                f"Gusset Mismatch: Limb holds {held} sts, but body skips {skipped} sts."
            )
        return errors

    def lint(self, text: str) -> list[str]:
        """Scan lines that state all four assembly numbers."""
        errors: list[str] = []
        pattern = re.compile(
            r"prev(?:ious)?[_\s-]*body\s*[:=]?\s*(\d+)"
            r".{0,80}?work(?:ed)?\s*[:=]?\s*(\d+)"
            r".{0,80}?skip(?:ped)?\s*[:=]?\s*(\d+)"
            r".{0,80}?(?:limb[_\s-]*)?h[oe]ld\s*[:=]?\s*(\d+)",
            re.IGNORECASE,
        )
        for line in text.splitlines():
            match = pattern.search(line)
            if not match:
                continue
            errors.extend(
                self.validate_socket_join(
                    int(match.group(1)),
                    int(match.group(2)),
                    int(match.group(3)),
                    int(match.group(4)),
                )
            )
        return _unique(errors)


class FabricDensityCalculator:
    """Compare stitch counts with a stated gauge. Estimates only."""

    def __init__(self, sts_per_in, rnds_per_in):
        self.sts_per_in = float(sts_per_in)
        self.rnds_per_in = float(rnds_per_in)
        if self.sts_per_in <= 0 or self.rnds_per_in <= 0:
            raise ValueError("Gauge must be positive.")

    def check_edging_density(self, edging_sts, target_row_ends):
        if target_row_ends <= 0 or edging_sts < 0:
            return None
        edge_length_in = target_row_ends / self.rnds_per_in
        edging_length_in = edging_sts / self.sts_per_in
        if edge_length_in <= 0:
            return None
        fullness_ratio = edging_length_in / edge_length_in
        if fullness_ratio > 2.5:
            return (
                f"Frill Alert: Edging is {fullness_ratio:.1f}x full "
                f"(threshold 2.5x). Fabric will bunch severely."
            )
        return None

    def check_attachment_span(self, seam_sts, body_rnds):
        if seam_sts < 0 or body_rnds < 0:
            return None
        seam_length_in = seam_sts / self.sts_per_in
        body_span_in = body_rnds / self.rnds_per_in
        small = min(seam_length_in, body_span_in)
        if small <= 0:
            return None
        ratio = max(seam_length_in, body_span_in) / small
        if ratio > 1.25:
            return (
                f"Span Mismatch: Seam ({seam_length_in:.2f}\") and body span "
                f"({body_span_in:.2f}\") differ by factor of {ratio:.1f}x."
            )
        return None

    @classmethod
    def scan(cls, text: str) -> list[str]:
        """Warn only when the pattern states a gauge and a measured edge or seam."""
        gauge = _GAUGE.search(text)
        if not gauge:
            return []
        inches = float(gauge.group(3))
        if inches <= 0:
            return []
        checker = cls(float(gauge.group(1)) / inches, float(gauge.group(2)) / inches)
        warnings = []
        for match in _EDGING.finditer(text):
            message = checker.check_edging_density(int(match.group(1)), int(match.group(2)))
            if message:
                warnings.append(message)
        for match in _SEAM.finditer(text):
            message = checker.check_attachment_span(int(match.group(1)), int(match.group(2)))
            if message:
                warnings.append(message)
        return _unique(warnings)


_GAUGE = re.compile(
    r"gauge\s*:\s*(\d+(?:\.\d+)?)\s*(?:sc|sts?|stitches)\s*(?:and|,)\s*"
    r"(\d+(?:\.\d+)?)\s*(?:rows?|rnds?|rounds?)\s*=\s*"
    r"(\d+(?:\.\d+)?)\s*(?:in|inch|inches)\b",
    re.IGNORECASE,
)
_EDGING = re.compile(
    r"(?:edging|border)\s*:\s*(\d+)\s*(?:sc|sts?|stitches)\b.{0,60}?"
    r"(\d+)\s*row[-\s]?ends?",
    re.IGNORECASE,
)
_SEAM = re.compile(
    r"seam\s*:\s*(\d+)\s*(?:sc|sts?|stitches)\b.{0,60}?"
    r"(\d+)\s*(?:body\s+)?(?:rnds?|rounds?|rows?)\b",
    re.IGNORECASE,
)


def _unique(items: list[str]) -> list[str]:
    found: list[str] = []
    for item in items:
        if item not in found:
            found.append(item)
    return found
