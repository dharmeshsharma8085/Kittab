from embedder import Embedder
from vector_store import VectorStore


# ============================================================
# VECTOR STORE TEST
# ============================================================

print(
    "\nKITTAB VECTOR STORE TEST"
)

print(
    "=" * 60
)


# ============================================================
# SAMPLE DOCUMENTS
# ============================================================

texts = [
    "RAG retrieves relevant information before generating an answer.",
    "Vector databases store numerical embeddings.",
    "Embeddings represent text as numerical vectors."
]


# ============================================================
# CREATE EMBEDDER
# ============================================================

embedder = Embedder()


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

print(
    "\nCreating embeddings..."
)

embeddings = embedder.embed_texts(
    texts
)


print(
    f"Created {len(embeddings)} embeddings."
)


# ============================================================
# CREATE VECTOR STORE
# ============================================================

store = VectorStore()


# ============================================================
# ADD DOCUMENTS
# ============================================================

store.add_documents(
    texts=texts,
    embeddings=embeddings,
    metadatas=[
        {
            "source_type": "test",
            "source": "sample_1"
        },
        {
            "source_type": "test",
            "source": "sample_2"
        },
        {
            "source_type": "test",
            "source": "sample_3"
        }
    ]
)


# ============================================================
# COUNT
# ============================================================

print(
    "\nDocuments stored:"
)

print(
    store.count()
)


# ============================================================
# SEARCH
# ============================================================

query = (
    "How does RAG retrieve information?"
)

print(
    "\nQuery:"
)

print(
    query
)


query_embedding = embedder.embed_text(
    query
)


results = store.search(
    query_embedding=query_embedding,
    n_results=2
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print(
    "\nSEARCH RESULTS"
)

print(
    "=" * 60
)


documents = results.get(
    "documents",
    [[]]
)[0]

distances = results.get(
    "distances",
    [[]]
)[0]


for i, document in enumerate(
    documents
):

    print(
        f"\nResult {i + 1}"
    )

    print(
        "-" * 40
    )

    print(
        document
    )

    if i < len(distances):

        print(
            f"Distance: "
            f"{distances[i]}"
        )


print(
    "\nVector store test completed."
)