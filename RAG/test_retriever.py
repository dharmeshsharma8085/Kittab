from embedder import Embedder
from vector_store import VectorStore
from retriever import Retriever


# ============================================================
# RETRIEVER TEST
# ============================================================

print(
    "\nKITTAB RETRIEVER TEST"
)

print(
    "=" * 60
)


# ============================================================
# SAMPLE DATA
# ============================================================

texts = [
    "RAG retrieves relevant information before generating an answer.",
    "Vector databases store numerical embeddings.",
    "Embeddings convert text into numerical vectors.",
    "Machine learning models learn patterns from data."
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
    },
    {
        "source_type": "ocr",
        "source": "handwritten_notes.jpg"
    }
]


# ============================================================
# CREATE COMPONENTS
# ============================================================

embedder = Embedder()

vector_store = VectorStore()


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

print(
    "\nCreating embeddings..."
)

embeddings = embedder.embed_texts(
    texts
)


# ============================================================
# ADD DATA
# ============================================================

vector_store.add_documents(
    texts=texts,
    embeddings=embeddings,
    metadatas=metadatas
)


# ============================================================
# CREATE RETRIEVER
# ============================================================

retriever = Retriever(
    embedder=embedder,
    vector_store=vector_store
)


# ============================================================
# QUERY
# ============================================================

query = (
    "How does RAG retrieve information?"
)

print(
    "\nQUERY"
)

print(
    "=" * 60
)

print(
    query
)


# ============================================================
# RETRIEVE
# ============================================================

results = retriever.retrieve(
    query=query,
    n_results=3
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print(
    "\nRETRIEVED RESULTS"
)

print(
    "=" * 60
)


for i, result in enumerate(
    results,
    start=1
):

    print(
        f"\nResult {i}"
    )

    print(
        "-" * 40
    )

    print(
        f"Text:\n{result['text']}"
    )

    print(
        f"\nMetadata:"
    )

    print(
        result["metadata"]
    )

    print(
        f"\nDistance:"
    )

    print(
        result["distance"]
    )


# ============================================================
# BUILD CONTEXT
# ============================================================

context = retriever.build_context(
    query=query,
    n_results=3
)


print(
    "\nRAG CONTEXT"
)

print(
    "=" * 60
)

print(
    context
)


print(
    "\nRetriever test completed."
)