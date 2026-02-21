import ollama


EMBED_MODEL = "nomic-embed-text"


def generate_embedding(text: str) -> list[float]:
    response = ollama.embeddings(
        model=EMBED_MODEL,
        prompt=text
    )

    return response["embedding"]


if __name__ == "__main__":
    test_text = "Alphawave provides AI consulting and digital solutions."

    embedding = generate_embedding(test_text)

    print("Embedding generated!")
    print(f"Vector length: {len(embedding)}")
    print("First 5 values:", embedding[:5])