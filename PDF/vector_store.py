import chromadb
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(
        self,
        collection_name: str = "kittab_documents",
        persist_directory: str = "../storage/chroma_db"
    ):
        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_chunks(self, chunks):
        if not chunks:
            return

        ids = [f"chunk_{i}" for i in range(len(chunks))]

        embeddings = self.embedding_model.encode(
            chunks,
            convert_to_numpy=True
        ).tolist()

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings
        )

        print(f"Added {len(chunks)} chunks to ChromaDB.")

    def search(self, query: str, top_k: int = 3):
        query_embedding = self.embedding_model.encode(
            query,
            convert_to_numpy=True
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results