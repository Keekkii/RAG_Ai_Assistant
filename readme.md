# AlphaWave AI Assistant 🌊

AlphaWave is a professional, self-hosted RAG (Retrieval-Augmented Generation) platform. It combines a high-performance Python/PostgreSQL backend with a premium React frontend to deliver secure, context-aware AI interactions.

## 🚀 Key Features

### Intelligent AI & RAG Layer
- **Local LLM**: Powered by **Ollama (Llama 3)** for grounded, private response generation.
- **Semantic Embeddings**: Uses `nomic-embed-text` (768 dimensions) for superior document understanding.
- **Vector Search**: High-performance **Cosine Distance** similarity matching using **pgvector**.
- **Hybrid Search**: Combines semantic vector retrieval with keyword-based filtering for maximum accuracy.
- **Automated Data Ingestion**: Built-in scraper using **BeautifulSoup** and **Requests** to build your knowledge base.

### Professional UI/UX
- **Dual-Interface System**:
  - **Floating Assistant Widget**: Minimalist, corporate-style popup for quick queries.
  - **Full-Screen Command Center**: Large-scale interface for deep interactions.
- **Responsive & Premium Design**: Enterprise SaaS aesthetic with glassmorphism, micro-animations, and full mobile support.
- **Client-Server Separation**: Modern REST API architecture ensuring scalability and clean boundaries.

---

## 🛠️ Tech Stack

### Backend
- **Core**: Python 3, FastAPI, Uvicorn (ASGI)
- **Database**: PostgreSQL 18 with **pgvector** (running via Docker)
- **Database Driver**: `psycopg2`
- **Configuration**: `python-dotenv` for environment isolation

### AI / RAG
- **LLM Engine**: Ollama (llama3)
- **Embeddings**: nomic-embed-text (Vector size: 768)
- **Logic**: Custom Python RAG implementation with semantic retrieval

### Frontend
- **Framework**: React (Vite)
- **State Management**: React Hooks (useState, useEffect, useRef)
- **Styling**: Vanilla CSS (Responsive, Modern UI)
- **Communication**: Fetch API

---

## 📦 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js & npm
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.com/) (installed and running)

### 2. Database Setup
The database runs as a containerized PostgreSQL 18 instance with vector capabilities:

```bash
docker run --name alphawave-db \
  -e POSTGRES_DB=alphawave_ai \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5433:5432 \
  -d ankane/pgvector
```

### 3. AI Models Setup
Pull the required models via Ollama:
```bash
ollama pull llama3
ollama pull nomic-embed-text
```

### 4. Backend Setup
1. **Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
2. **Installation**:
   ```bash
   pip install fastapi uvicorn ollama pydantic beautifulsoup4 requests psycopg2-binary python-dotenv
   ```
3. **Execution**:
   ```bash
   uvicorn app.api:app --reload
   ```

### 5. Frontend Setup
1. **Installation**:
   ```bash
   cd frontend
   npm install
   ```
2. **Execution**:
   ```bash
   npm run dev
   ```

---

## 📂 Project Structure

```text
├── app/                # Backend Application
│   ├── api.py          # FastAPI Endpoints
│   ├── rag.py          # RAG & LLM Logic
│   ├── database.py     # PostgreSQL & pgvector Logic
│   ├── embeddings.py   # Embedding Generation (size: 768)
│   └── scraper.py      # BeautifulSoup Data Ingestion
├── frontend/           # React Frontend
│   ├── src/
│   │   ├── ChatWidget  # Professional Floating UI
│   │   └── FullChat    # Large Screen UI
├── docs/               # Local Knowledge Documents
└── readme.md           # Documentation
```

---

## 🔒 Security & Data Sovereignty
AlphaWave is a **fully self-hosted** solution. By using local Docker containers and local LLM instances (Ollama), your data never leaves your infrastructure, providing absolute privacy and control over your grounded AI responses.
