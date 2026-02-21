import psycopg2
from psycopg2.extras import RealDictCursor
from app.embeddings import generate_embedding


DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "alphawave_ai",
    "user": "postgres",
    "password": "postgres"
}


def get_connection():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        cursor_factory=RealDictCursor
    )


# -------------------------
# Keyword extraction (simple)
# -------------------------
def extract_keywords(query: str):
    words = query.split()
    # remove very short words like "is", "the", "of"
    return [w.strip("?,.!") for w in words if len(w) > 3]


# -------------------------
# Insert document
# -------------------------
def insert_document(url: str, title: str, content: str):
    embedding = generate_embedding(content)
    vector_str = "[" + ",".join(map(str, embedding)) + "]"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO documents (url, title, content, embedding)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (url, title, content, vector_str))

    new_id = cursor.fetchone()["id"]
    conn.commit()

    cursor.close()
    conn.close()

    return new_id


# -------------------------
# Hybrid search
# -------------------------
def search_similar_documents(query: str, limit: int = 5):
    embedding = generate_embedding(query)
    vector_str = "[" + ",".join(map(str, embedding)) + "]"

    keywords = extract_keywords(query)

    like_clauses = []
    params = []

    for word in keywords:
        like_clauses.append("(title ILIKE %s OR content ILIKE %s)")
        params.extend([f"%{word}%", f"%{word}%"])

    keyword_sql = " OR ".join(like_clauses) if like_clauses else "FALSE"

    conn = get_connection()
    cursor = conn.cursor()

    sql = f"""
    SELECT id, url, title, content,
           embedding <=> %s AS distance
    FROM documents
    WHERE embedding IS NOT NULL
    ORDER BY
        CASE
            WHEN ({keyword_sql}) THEN 0
            ELSE 1
        END,
        embedding <=> %s
    LIMIT %s;
    """

    cursor.execute(sql, [vector_str] + params + [vector_str, limit])

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results


# -------------------------
# Manual test
# -------------------------
if __name__ == "__main__":
    try:
        query = "What is the DPP-Compliant Asset Management Platform?"

        results = search_similar_documents(query)

        print("\nSearch Results:\n")
        for r in results:
            print(f"ID: {r['id']}")
            print(f"Title: {r['title']}")
            print(f"Distance: {r['distance']}")
            print(f"Content Preview: {r['content'][:150]}...")
            print("-" * 50)

    except Exception as e:
        print("Operation failed:")
        print(e)