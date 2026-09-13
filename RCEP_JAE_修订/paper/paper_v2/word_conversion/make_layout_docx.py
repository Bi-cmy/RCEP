from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt


ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"
OUTPUT = ROOT.parent / "main_english_v2_layout.docx"


def main() -> None:
    pages = sorted(PAGES.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
    if not pages:
        raise SystemExit(f"No rendered PDF pages found in {PAGES}")

    document = Document()
    section = document.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0)
    section.bottom_margin = Inches(0)
    section.left_margin = Inches(0)
    section.right_margin = Inches(0)
    section.header_distance = Inches(0)
    section.footer_distance = Inches(0)

    for index, page in enumerate(pages):
        if index:
            section = document.add_section(WD_SECTION.NEW_PAGE)
            section.page_width = Inches(8.5)
            section.page_height = Inches(11)
            section.top_margin = Inches(0)
            section.bottom_margin = Inches(0)
            section.left_margin = Inches(0)
            section.right_margin = Inches(0)
            section.header_distance = Inches(0)
            section.footer_distance = Inches(0)
            # ``add_section`` creates the paragraph that carries the section
            # break. Reuse it for the page image so no blank paragraph is
            # inserted before each page.
            paragraph = document.paragraphs[-1]
        else:
            paragraph = document.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.paragraph_format.line_spacing = 1
        run = paragraph.add_run()
        run.add_picture(str(page), width=Inches(8.5), height=Inches(11))

    core = document.core_properties
    core.title = "RCEP and Supply Chain Relationships of Chinese Firms"
    core.subject = "Layout-preserving Word version of the English manuscript"
    core.author = "Anonymous manuscript"
    document.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
