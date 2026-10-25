"""Pack all 17 Novality patterns into one distributable zip (run from repo root)."""
import pathlib, zipfile, sys

ROOT = pathlib.Path(".")
NUMS = ["01", "02", "03", "04", "05", "06", "07", "08", "09",
        "10", "11", "12", "13", "14", "15", "16", "17"]
out = ROOT / "NovalityStore_All_17_Patterns.zip"
if out.exists():
    out.unlink()
count = 0
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for n in NUMS:
        d = ROOT / f"docs/ns{n}"
        md = d / f"NS{n}_corrected.md"
        rep = d / f"NS{n}_validation_report.md"
        spec = d / "spec.py"
        files = [md, rep]
        ns = {"__file__": str(spec)}
        exec(compile(spec.read_text(), str(spec), "exec"), ns)
        S = ns["SPEC"]
        files += [ROOT / S["out"], ROOT / S["out_bw"]]
        for f in files:
            if not f.exists():
                raise SystemExit(f"missing {f}")
            z.write(f, f"NS-{n}/{f.name}")
            count += 1
    z.write(ROOT / "docs/kit/audit_lib.py", "VERIFICATION/audit_lib.py")
    z.write(ROOT / "docs/kit/audit_overrides.py", "VERIFICATION/audit_overrides.py")
    z.write(ROOT / "docs/kit/build_store_pdf.py", "VERIFICATION/build_store_pdf.py")
    count += 3
print("zip written:", out, out.stat().st_size, "bytes,", count, "files")
