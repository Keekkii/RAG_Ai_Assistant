from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from app.database import search_similar_documents

LLM_MODEL = "qwen2.5:7b"

llm = ChatOllama(model=LLM_MODEL)

RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are an AI assistant for AlphaWave.

Answer the question using ONLY the context below. 
Provide a helpful, natural summary based on the context.
If the answer is not contained in the context, say "I don't know."

Context:
{context}

Question:
{question}

Answer:"""
)

# Modern LCEL chain: prompt | llm | output parser
chain = RAG_PROMPT | llm | StrOutputParser()


def normalize_question(question: str) -> str:
    normalized = question.strip()
    if len(normalized.split()) < 3:
        return f"Explain {normalized}"
    return normalized



import time
from app.logger import log_interaction

def generate_answer(question: str, user_email: str = "Anonymous", user_name: str = "Guest") -> str:
    start_time = time.time()
    normalized_question = normalize_question(question)
    
    # Use the fast, high-quality RRF hybrid search
    # retrieving 7 chunks instead of 5 to be safe, but still fast
    print(f"\nPerforming fast RRF search for: {normalized_question}")
    results = search_similar_documents(normalized_question, limit=7)
    
    if not results:
        return "I don't know."

    print("\nRetrieved Chunks (RRF Ranked):\n")
    for r in results:
        print(f"TITLE: {r['title']}")
        print(f"RRF SCORE: {r.get('rrf_score', 0):.4f}")
        # print("CONTENT PREVIEW:", r["content"][:100])
        print("-" * 50)
        
    # Go through every result we found in the database, 
    # grab just the text content, and put it into a new list of strings.
    context = "\n\n".join([r["content"] for r in results])

    # Only one LLM call now - for the final answer!
    answer = chain.invoke({"context": context, "question": normalized_question})
    
    elapsed_time = (time.time() - start_time) * 1000  # ms
    
    # Log the interaction for the dashboard
    log_interaction(
        query=question,
        normalized_query=normalized_question,
        results=results,
        answer=answer,
        latency_ms=elapsed_time,
        user_email=user_email,
        user_name=user_name
    )

    return answer


if __name__ == "__main__":
    question = "What is the UNIRI Sports Center AI Assistant?"
    answer = generate_answer(question)
    print("\nAI Answer:\n")
    print(answer)
