def chunk_text(text: str, chunk_size: int = 400, overlap: int = 100) -> list[str]:
    """
    Splits text into overlapping chunks.

    :param text: Full text to split
    :param chunk_size: Maximum size of each chunk (in characters)
    :param overlap: Number of overlapping characters between chunks
    :return: List of text chunks
    """

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        # Move start forward but keep overlap
        start += chunk_size - overlap

    return chunks

"""
if __name__ == "__main__":
    sample_text = "A" * 2000  # simulate long text
    chunks = chunk_text(sample_text)

    print(f"Total chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1} length: {len(chunk)}")"""