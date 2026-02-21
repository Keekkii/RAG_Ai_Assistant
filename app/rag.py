from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from app.database import search_similar_documents

LLM_MODEL = "llama3"

llm = ChatOllama(model=LLM_MODEL)

RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are an AI assistant for AlphaWave.

Answer the question using ONLY the context below.
If the answer is not contained in the context, say "I don't know."

Context:
{context}

Question:
{question}

Answer:"""
)

# Modern LCEL chain: prompt | llm | output parser
chain = RAG_PROMPT | llm | StrOutputParser()


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

    return chain.invoke({"context": context, "question": question})


if __name__ == "__main__":
    question = "What is the UNIRI Sports Center AI Assistant?"
    answer = generate_answer(question)
    print("\nAI Answer:\n")
    print(answer)