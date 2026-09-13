from pathlib import Path

from docx import Document
from docx.oxml.ns import qn


ROOT = Path(__file__).resolve().parent
PATH = ROOT.parent / "main_english_v2_editable.docx"


def set_font(font) -> None:
    font.name = "Times New Roman"
    font._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    font._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    font._element.rPr.rFonts.set(qn("w:cs"), "Times New Roman")
    font._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")


def main() -> None:
    document = Document(PATH)

    # Apply the manuscript font to all paragraph, character, and table styles.
    for style in document.styles:
        if style.font is not None:
            set_font(style.font)

    # Section headings and table/figure captions are conventionally bold.
    for style_name in ("Heading 1", "Heading 2", "Heading 3", "Table Caption"):
        if style_name in [s.name for s in document.styles]:
            document.styles[style_name].font.bold = True

    def format_paragraph(paragraph) -> None:
        for run in paragraph.runs:
            set_font(run.font)

    for paragraph in document.paragraphs:
        format_paragraph(paragraph)
        if paragraph.style.name in ("Heading 1", "Heading 2", "Heading 3", "Table Caption"):
            for run in paragraph.runs:
                run.bold = True
        if paragraph.style.name == "Image Caption" and paragraph.text.strip() and not paragraph.text.lstrip().startswith("Notes:"):
            for run in paragraph.runs:
                run.bold = True
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    format_paragraph(paragraph)

    document.save(PATH)
    print(PATH)


if __name__ == "__main__":
    main()
