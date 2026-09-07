# Axel the Axolotl - publishing kit

Everything generated for the **Axel the Axolotl** pattern (Novality Store, Design NS 03), built from one
verified data file so the PDF, audio, video and Etsy copy never disagree on a stitch count.

| Deliverable | Path | Notes |
|---|---|---|
| Designed pattern PDF | `Axel_the_Axolotl_Pattern.pdf` | 12 pages, A4, 1.8 MB. Cover, materials, 5 techniques, every round in tables, assembly, troubleshooting, colourways, terms. |
| Audio walkthrough | `audio/Axel_the_Axolotl_Full_Walkthrough.mp3` + `audio/01..10_*.mp3` | ~12 min narrated, 10 chapters. Every round read out with its stitch count. |
| Tutorial video | `video/Axel_the_Axolotl_Tutorial.mp4` + `video/chapters.txt` | 1080p H.264/AAC, 12:06. Round-by-round slides; the row being spoken is highlighted; captions; chapter markers for YouTube. |
| Etsy listing kit | `etsy/01..10_*.jpg`, `etsy/LISTING_COPY.md`, `etsy/listing.json` | Ten 2000x2000 listing images in upload order, plus title (SEO), 13 tags, description, FAQ, shop announcement and buyer message. |
| Photos | `assets/img/` | AI-generated product photography (hero, gill/tail details, materials flat lay, WIP, scale-in-hand, 5 colourways). Replace with real photos of a finished sample before selling - buyers expect the real toy. |

## Rebuild

```bash
python -m venv .venv && .venv/bin/pip install reportlab pillow imageio-ffmpeg pymupdf
cd axel_kit/scripts
python build_pdf.py     # -> ../Axel_the_Axolotl_Pattern.pdf
python build_video.py   # -> ../video/Axel_the_Axolotl_Tutorial.mp4  (needs audio/*.mp3)
python build_etsy.py    # -> ../etsy/
```

`pattern_data.py` is the single source of truth for every instruction, count and note; `narration.py` holds
the spoken script. Edit those, re-run the three builders.

## Verification

All 52 rounds (body 36, arms 6, feet 5, gills 5) pass `crochet-check` with 0 stitch-count errors, and were
cross-checked by hand. Dimensions in the pattern match its own gauge (36 sts x 4.5 mm / pi = 51.6 mm head).

## Fonts

Fredoka One, Source Sans Pro and Caladea - all SIL Open Font License (see `assets/fonts/OFL-*.txt`).
Free for commercial use, embedding and redistribution inside the PDF.

## Etsy upload notes

- Etsy allows 20 MB per digital file. The PDF and MP3s fit; the 22 MB video does not - host it unlisted on
  YouTube/Vimeo and put the link plus `video/chapters.txt` on the PDF's last page (or in a one-page "links" PDF).
- Upload the ten images in numeric order; `01_cover.jpg` is designed to read at Etsy's 270 px grid thumbnail.
- The description clearly states it is a digital file with no shipping (required for Etsy digital listings).
