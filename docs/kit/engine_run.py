"""Run the repo verification engine over a pattern file and print findings."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
from crochet_checker.verification.stages import run_stages

path = pathlib.Path(sys.argv[1])
rep = run_stages(path.read_text(encoding="utf-8"))
errs = getattr(rep, "errors", None)
warns = getattr(rep, "warnings", None)
if errs is None:
    print(rep)
else:
    print(f"ERRORS ({len(errs)}):")
    for e in errs: print("  -", e)
    print(f"WARNINGS ({len(warns)}):")
    for w in warns: print("  -", w)
