from embedder import Embedder
from vector_store import VectorStore
from retriever import Retriever
from rag_engine import RAGEngine


# ============================================================
# RAG ENGINE TEST
# ============================================================

print(
    "\nKITTAB RAG ENGINE TEST"
)

print(
    "=" * 60
)


# ============================================================
# SAMPLE KNOWLEDGE
# ============================================================

texts = [
    (
        "Retrieval-Augmented Generation (RAG) "
        "combines information retrieval with "
        "large language models. It retrieves "
        "relevant documents before generating "
        "an answer."
    ),

    (
        "Vector databases store numerical "
        "representations called embeddings. "
        "They allow semantic similarity search."
    ),

    (
        "Embeddings convert text into numerical "
        "vectors that capture semantic meaning."
    )
]


metadatas = [
    {
        "source_type": "pdf",
        "source": "rag_notes.pdf"
    },
    {
        "source_type": "web",
        "source": "example.com"
    },
    {
        "source_type": "audio",
        "source": "lecture.mp3"
    }
]


# ============================================================
# CREATE COMPONENTS
# ============================================================

embedder = Embedder()

vector_store = VectorStore()


# ============================================================
# EMBEDDINGS
# ============================================================

print(
    "\nCreating embeddings..."
)

embeddings = embedder.embed_texts(
    texts
)


# ============================================================
# STORE DOCUMENTS
# ============================================================

vector_store.add_documents(
    texts=texts,
    embeddings=embeddings,
    metadatas=metadatas
)


# ============================================================
# RETRIEVER
# ============================================================

retriever = Retriever(
    embedder=embedder,
    vector_store=vector_store
)


# ============================================================
# RAG ENGINE
# ============================================================

rag = RAGEngine(
    retriever=retriever,
    top_k=3
)


# ============================================================
# USER QUESTION
# ============================================================

query = (
    "What is RAG and how does it work?"
)


print(
    "\nQUESTION"
)

print(
    "=" * 60
)

print(
    query
)


# ============================================================
# ASK
# ============================================================

result = rag.ask_with_sources(
    query
)


# ============================================================
# ANSWER
# ============================================================

print(
    "\nANSWER"
)

print(
    "=" * 60
)

print(
    result["answer"]
)


# ============================================================
# SOURCES
# ============================================================

print(
    "\nSOURCES"
)

print(
    "=" * 60
)

for source in result["sources"]:

    print(
        f"\nType: "
        f"{source['source_type']}"
    )

    print(
        f"Source: "
        f"{source['source']}"
    )


print(
    "\nRAG Engine test completed."
)