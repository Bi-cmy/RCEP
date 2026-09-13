from pathlib import Path

from docx import Document
from docx.shared import Inches


ROOT = Path(__file__).resolve().parent
INPUT = ROOT.parent / "main_english_v2_editable.docx"
OUTPUT = ROOT.parent / "main_english_v2_editable.docx"


def main() -> None:
    document = Document(INPUT)
    indent = Inches(0.28)
    for style_name in ("First Paragraph", "Body Text"):
        style = document.styles[style_name]
        style.paragraph_format.first_line_indent = indent
    document.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
