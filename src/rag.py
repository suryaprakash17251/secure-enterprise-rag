from qdrant_client import models
from rbac import allowed_departments
from langchain_groq import ChatGroq

from config import GROQ_API_KEY
from vectorstore import get_store

llm = ChatGroq(model="openai/gpt-oss-20b", api_key=GROQ_API_KEY, temperature=0)
store = get_store()

PROMPT = """You are a company assistant. Answer the question using ONLY the context below.
If the answer is not in the context, say you don't have that information.

Context:
{context}

Question: {question}
Answer:"""


def answer(question: str, role: str, k: int = 8):
    depts = allowed_departments(role)
    if not depts:
        return "Access denied: unknown role.", []

    flt = models.Filter(must=[
        models.FieldCondition(
            key="metadata.department",
            match=models.MatchAny(any=depts),
        )
    ])
    docs = store.similarity_search(question, k=k, filter=flt)
    context = "\n\n".join(
        f"[{d.metadata['source']} | {d.metadata['department']}]\n{d.page_content}"
        for d in docs
    )
    resp = llm.invoke(PROMPT.format(context=context, question=question))
    return resp.content, docs


if __name__ == "__main__":
    role = input("Role (finance/hr/marketing/engineering/employee/c_level): ").strip()
    while True:
        q = input("\nAsk (or 'quit'): ").strip()
        if q.lower() in {"quit", "exit", ""}:
            break
        ans, docs = answer(q, role)
        print("\n" + ans)
        print("\nSources:", {(d.metadata["source"], d.metadata["department"]) for d in docs})