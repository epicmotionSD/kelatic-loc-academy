"""
Rebuild the-blueprint-vault-9He2Kx.pdf with a revised Introduction.

The book shipped without a source document. This script reconstructs it from
the original PDF plus a freshly rendered Introduction:

    pages  1-4   front matter + contents   (from the original, untouched)
    pages  5-..  the new Introduction      (from book/intro.pdf)
    rest         chapters I-XII            (original pages 8-53)

The original numbered pages 5-53 as folios 1-49. Replacing a 3-page
Introduction with a longer one shifts every later folio, so the corrected
numbers are stamped over the old ones from book/folio-overlay.pdf, whose silk
patch hides the original digit.

Usage:
    python book/splice-intro.py

Inputs  : the-blueprint-vault-9He2Kx.pdf, book/intro.pdf, book/folio-overlay.pdf,
          book/silk.pdf
Output  : the-blueprint-vault-9He2Kx.pdf (rewritten in place after a backup)
"""

import io
import shutil
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "the-blueprint-vault-9He2Kx.pdf"
INTRO = ROOT / "book" / "intro.pdf"
OVERLAY = ROOT / "book" / "folio-overlay.pdf"
SILK = ROOT / "book" / "silk.pdf"
BACKUP = ROOT / "book" / "the-blueprint-vault-ORIGINAL.pdf"

# Original layout (1-based): front matter 1-4, Introduction 5-7, Chapter I from 8.
FRONT_MATTER_END = 4
OLD_INTRO_PAGES = (5, 7)
FIRST_CHAPTER_PAGE = 8


def main() -> int:
    for p in (BOOK, INTRO, OVERLAY, SILK):
        if not p.exists():
            print(f"missing input: {p}")
            return 1

    if not BACKUP.exists():
        shutil.copy2(BOOK, BACKUP)
        print(f"backed up original -> {BACKUP.name}")

    src = PdfReader(str(BACKUP))          # always build from the pristine original
    intro = PdfReader(str(INTRO))
    overlay = PdfReader(str(OVERLAY))

    print(f"original: {len(src.pages)} pages | new intro: {len(intro.pages)} pages")

    writer = PdfWriter()

    # 1. Front matter, unchanged.
    for i in range(FRONT_MATTER_END):
        writer.add_page(src.pages[i])

    # 2. New Introduction in place of old pages 5-7.
    #    The rendered Introduction is text on a transparent ground, so each page
    #    is composited over a full-bleed silk sheet. A fresh reader per page
    #    because merge_page mutates the base it draws onto.
    for page in intro.pages:
        base = PdfReader(str(SILK)).pages[0]
        base.merge_page(page, over=True)
        writer.add_page(base)

    # 3. Chapter I onward.
    for i in range(FIRST_CHAPTER_PAGE - 1, len(src.pages)):
        writer.add_page(src.pages[i])

    total = len(writer.pages)
    numbered = total - FRONT_MATTER_END
    print(f"rebuilt: {total} pages ({numbered} numbered)")

    if numbered > len(overlay.pages):
        print(f"overlay has {len(overlay.pages)} sheets, need {numbered}")
        return 1

    # 4. Stamp corrected folios over every numbered page.
    for n in range(numbered):
        page = writer.pages[FRONT_MATTER_END + n]
        page.merge_page(overlay.pages[n], over=True)

    with open(BOOK, "wb") as fh:
        writer.write(fh)

    print(f"wrote {BOOK.name}: {total} pages, folios 1-{numbered}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
