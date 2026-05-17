# CampusGPT — Backend

## Tech Stack

| Layer | Technology |
|---|---|
| Server | Python, Flask |
| Vector Store | ChromaDB |
| Embeddings | Sentence Transformers |
| LLM | Groq API |
| RAG Framework | LangChain |
| PDF Parsing | PyMuPDF |
| OCR | Tesseract |

---

## Retrieval Workflow

```
User Query
    ↓
Embedding Generation
    ↓
ChromaDB Semantic Retrieval
    ↓
Metadata Extraction
    ↓
LLM Response Generation (Groq)
    ↓
Official Verification Links
```

1. **Query comes in** via `POST /chat`
2. **Embedding model** converts the query into a vector
3. **ChromaDB** performs semantic search across indexed question papers
4. **Metadata extractor** pulls subject, college, and filename from matched chunks
5. **Groq LLM** generates a natural language answer from retrieved context
6. **Response** includes the answer, source PDF filenames, and official verification links
