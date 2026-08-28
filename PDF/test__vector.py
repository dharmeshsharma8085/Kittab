from pdf_loader import extract_text_from_pdf
from chunker import chunk_text
from vector_store import VectorStore


PDF_PATH = r"C:\Users\DHARMESH SHARMA\Downloads\DSA_for_AI_Engineers.pdf"


# PDF → Text
text = extract_text_from_pdf(PDF_PATH)

# Text → Chunks
chunks = chunk_text(text)

print(f"Created {len(chunks)} chunks")


# Chunks → Embeddings → ChromaDB
store = VectorStore()

store.add_chunks(chunks)


# Test semantic search
query = "What is the time complexity of accessing an array?"

results = store.search(query, top_k=3)


print("\nSEARCH RESULTS")
print("=" * 60)

for i, document in enumerate(results["documents"][0], start=1):
    print(f"\nResult {i}")
    print("-" * 40)
    print(document)