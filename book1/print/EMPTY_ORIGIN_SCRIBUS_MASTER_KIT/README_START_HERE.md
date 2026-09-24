# Empty Origin — Scribus Master Kit

This folder is the plug-and-play production starter for the 6×9 interior.

1. Install Scribus + fonts using `FONT_SETUP_ARCH.md`.
2. Open `EMPTY_ORIGIN_MASTER.sla`.
3. Keep the approved chapter-opener sample PDF in the parent `book1/print/` folder open beside Scribus as the visual authority.
4. Page 1 is the chapter opener; pages 2–3 are normal body pages.
5. Duplicate body pages and link text frames as needed.
6. Use the named styles in Edit → Styles.

If the .sla gives trouble, run `scripts/create_empty_origin_master.py` inside Scribus via Script → Execute Script.

The generator reads Chapter 1 directly from `book1/chapters/chapter-01.md`.

Included: editable SLA, scalable aperture ring, style guide, pagination rules, export checklist, Arch setup, object map, and Scribus generator script.
