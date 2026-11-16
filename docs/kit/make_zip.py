"""Pack the 34 shop editions into one distributable zip (run from repo root).

Each pattern gets its own folder inside the archive:

    NS-01/NS01_Hamish_the_Highland_Cow_Colour_Edition.pdf
    NS-01/NS01_Hamish_the_Highland_Cow_Print_Edition.pdf
    ...

The archive is written to the repo root and is ignored by git; it is meant for
attaching to a GitHub release rather than for committing.
"""
import pathlib
import sys
import zipfile

ROOT = pathlib.Path(".")
SHOP = ROOT / "shop"
OUT = ROOT / "NovalityStore_All_17_Patterns.zip"


def main() -> int:
    pdfs = sorted(SHOP.glob("NS*_Colour_Edition.pdf")) + \
        sorted(SHOP.glob("NS*_Print_Edition.pdf"))
    if len(pdfs) != 34:
        print(f"expected 34 editions in shop/, found {len(pdfs)}", file=sys.stderr)
        return 1

    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for pdf in pdfs:
            code = pdf.name[:5].replace("NS", "NS-")   # NS01_Hamish… -> NS-01
            z.write(pdf, f"{code}/{pdf.name}")
        readme = SHOP / "README.md"
        if readme.exists():
            z.write(readme, "README.md")

    size = OUT.stat().st_size / 1e6
    print(f"wrote {OUT} ({len(pdfs)} editions, {size:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
