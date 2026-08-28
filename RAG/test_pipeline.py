from pipeline import RAGPipeline


# ============================================================
# PIPELINE TEST
# ============================================================

print(
    "\nKITTAB RAG PIPELINE TEST"
)

print(
    "=" * 60
)


# ============================================================
# SAMPLE TEXT
# ============================================================

text = """
Retrieval-Augmented Generation, or RAG,
combines information retrieval with a
large language model.

First, the system converts documents into
smaller chunks. These chunks are converted
into numerical embeddings and stored in a
vector database.

When a user asks a question, the question
is also converted into an embedding.
The system searches the vector database
for relevant chunks.

The retrieved information is then provided
to the language model as context so that
it can generate a grounded answer.
"""


# ============================================================
# CREATE PIPELINE
# ============================================================

pipeline = RAGPipeline(
    chunk_size=300,
    chunk_overlap=50
)


# ============================================================
# INGEST
# ============================================================

result = pipeline.ingest_text(
    text=text,
    source_type="test",
    source="sample_rag_notes.txt",
    metadata={
        "title": "RAG Sample Notes"
    }
)


# ============================================================
# RESULT
# ============================================================

print(
    "\nPIPELINE RESULT"
)

print(
    "=" * 60
)

print(
    f"Source type: "
    f"{result['source_type']}"
)

print(
    f"Source: "
    f"{result['source']}"
)

print(
    f"Characters: "
    f"{result['characters']}"
)

print(
    f"Chunks: "
    f"{result['chunks']}"
)

print(
    f"Embeddings: "
    f"{result['embeddings']}"
)

print(
    f"\nTotal chunks in ChromaDB: "
    f"{pipeline.count()}"
)

print(
    "\nPipeline test completed."
)