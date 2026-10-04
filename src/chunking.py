from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_SIZE, CHUNK_OVERLAP
from ingest import load_documents


def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "],
    )
    # split_documents copies each doc's metadata onto every chunk
    return splitter.split_documents(docs)


if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    print(f"{len(docs)} documents -> {len(chunks)} chunks")

    counts = {}
    for c in chunks:
        dept = c.metadata["department"]
        counts[dept] = counts.get(dept, 0) + 1
    print(counts)

    for c in chunks[:2] + chunks[-2:]:
        print("\n---", c.metadata)
        print(c.page_content[:200])