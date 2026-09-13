from pathlib import Path

from docx import Document


PATH = Path(__file__).resolve().parent.parent / "main_english_v2_editable.docx"


def main():
    document = Document(PATH)
    removed = 0
    for table in list(document.tables):
        if len(table.rows) == 0:
            table._element.getparent().remove(table._element)
            removed += 1
    document.save(PATH)
    print(f"removed={removed} path={PATH}")


if __name__ == "__main__":
    main()
