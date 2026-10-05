from qdrant_client.models import Distance, VectorParams
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


from config import QDRANT_URL, QDRANT_API_KEY
from chunking import chunk_documents
from ingest import load_documents

COLLECTION = "company_docs"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def build_index():
    chunks = chunk_documents(load_documents())
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=120)

    if client.collection_exists(COLLECTION):
        client.delete_collection(COLLECTION)
    client.create_collection(
        COLLECTION,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    store = QdrantVectorStore(client=client, collection_name=COLLECTION, embedding=embeddings)
    for i in range(0, len(chunks), 16):
        store.add_documents(chunks[i:i + 16])
        print(f"Uploaded {min(i + 16, len(chunks))}/{len(chunks)}")
    return store

def get_store():
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    return QdrantVectorStore(client=client, collection_name=COLLECTION, embedding=embeddings)


if __name__ == "__main__":
    build_index()
    print("Index built")