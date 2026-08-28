from embedder import Embedder


# ============================================================
# EMBEDDER TEST
# ============================================================

print(
    "\nKITTAB EMBEDDER TEST"
)

print(
    "=" * 60
)


# ============================================================
# CREATE EMBEDDER
# ============================================================

embedder = Embedder()


# ============================================================
# TEST SINGLE TEXT
# ============================================================

text = (
    "Retrieval Augmented Generation "
    "combines retrieval with language models."
)


embedding = embedder.embed_text(
    text
)


print(
    "\nSINGLE TEXT"
)

print(
    "=" * 60
)

print(
    f"Embedding dimension: "
    f"{len(embedding)}"
)

print(
    f"First 10 values:\n"
    f"{embedding[:10]}"
)


# ============================================================
# TEST MULTIPLE TEXTS
# ============================================================

texts = [
    "Machine learning learns patterns from data.",
    "Large language models generate natural language.",
    "Vector databases store embeddings."
]


embeddings = embedder.embed_texts(
    texts
)


print(
    "\nMULTIPLE TEXTS"
)

print(
    "=" * 60
)

print(
    f"Texts: {len(texts)}"
)

print(
    f"Embeddings: {len(embeddings)}"
)

print(
    f"Dimension: {len(embeddings[0])}"
)


print(
    "\nEmbedder test completed."
)