import ollama
from app.database import search_similar_documents

LLM_MODEL = "llama3"


def generate_answer(question: str) -> str:
    results = search_similar_documents(question, limit=10)
    print("\nRetrieved Chunks:\n")
    for r in results:
        print("TITLE:", r["title"])
        print("DISTANCE:", r["distance"])
        print("CONTENT PREVIEW:", r["content"][:200])
        print("-" * 50)


    if not results:
        return "I don't know."

    context = "\n\n".join([r["content"] for r in results])

    prompt = f"""
You are an AI assistant for AlphaWave.

Answer the question using ONLY the context below.
If the answer is not contained in the context, say "I don't know."

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    question = "What is the UNIRI Sports Center AI Assistant?"

    answer = generate_answer(question)

    print("\nAI Answer:\n")
    print(answer)