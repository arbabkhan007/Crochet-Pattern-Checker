"""Per-pattern expected counts for rows the generic grammar reports unparsed.
Keys are lower-cased row labels; None means 'continuation row, accept stated'."""
OVERRIDES = {
    "NS-07": {"petal": 36},
    "NS-10": {"rnd 2": 24, "rnds 3-20": None},
    "NS-11": {"r9-12": 30, "r13": 30, "r16": 30},
    "NS-15": {"join": None, "hanger": None, "petals": None, "leaves": None,
              "tie": None, "r3": None, "loops": None, "-": None},
}
SKIP_TABLES = {}
