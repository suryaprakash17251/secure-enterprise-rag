from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, CSVLoader

from config import DATA_DIR, DEPARTMENTS

TEXT_EXT = {".md", ".txt"}
DOCLING_EXT = {".pdf", ".docx", ".pptx", ".html"}


def get_department(path: Path) -> str:
    """Department = first folder under data/. Unknown folders -> 'general'."""
    rel = path.relative_to(DATA_DIR)
    folder = rel.parts[0] if len(rel.parts) > 1 else "general"
    return DEPARTMENTS.get(folder.lower(), "general")


def load_file(path: Path) -> list[Document]:
    ext = path.suffix.lower()

    if ext in TEXT_EXT:
        docs = TextLoader(str(path), encoding="utf-8").load()
    elif ext == ".csv":
        docs = CSVLoader(str(path), encoding="utf-8").load()
    elif ext in DOCLING_EXT:
        from docling.document_converter import DocumentConverter
        result = DocumentConverter().convert(str(path))
        text = result.document.export_to_markdown()
        docs = [Document(page_content=text)]
    else:
        return []  # unsupported file type, skip

    dept = get_department(path)
    for d in docs:
        d.metadata["department"] = dept
        d.metadata["source"] = path.name
    return docs


def load_documents() -> list[Document]:
    all_docs = []
    for path in sorted(DATA_DIR.rglob("*")):
        if path.is_file() and path.name != ".gitkeep":
            try:
                all_docs.extend(load_file(path))
            except Exception as e:
                print(f"Skipped {path.name}: {e}")
    return all_docs


if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")
    counts = {}
    for d in docs:
        counts[d.metadata["department"]] = counts.get(d.metadata["department"], 0) + 1
    print(counts)