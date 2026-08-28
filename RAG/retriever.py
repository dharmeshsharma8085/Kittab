from typing import List, Dict

from embedder import Embedder
from vector_store import VectorStore


# ============================================================
# RETRIEVER
# ============================================================

class Retriever:
    """
    Retrieve the most relevant document chunks
    from Kittab's ChromaDB vector store.
    """

    def __init__(
        self,
        embedder: Embedder = None,
        vector_store: VectorStore = None
    ):
        print(
            "\nInitializing Retriever..."
        )

        # ----------------------------------------------------
        # Embedding model
        # ----------------------------------------------------

        self.embedder = (
            embedder
            if embedder is not None
            else Embedder()
        )

        # ----------------------------------------------------
        # Vector store
        # ----------------------------------------------------

        self.vector_store = (
            vector_store
            if vector_store is not None
            else VectorStore()
        )

        print(
            "Retriever initialized successfully."
        )

    # ========================================================
    # RETRIEVE
    # ========================================================

    def retrieve(
        self,
        query: str,
        n_results: int = 5
    ) -> List[Dict]:
        """
        Retrieve the most relevant chunks for a query.
        """

        if not isinstance(
            query,
            str
        ):
            raise TypeError(
                "Query must be a string."
            )

        query = query.strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        if n_results < 1:
            raise ValueError(
                "n_results must be at least 1."
            )

        # ----------------------------------------------------
        # Create query embedding
        # ----------------------------------------------------

        query_embedding = (
            self.embedder.embed_text(
                query
            )
        )

        # ----------------------------------------------------
        # Search vector database
        # ----------------------------------------------------

        results = self.vector_store.search(
            query_embedding=query_embedding,
            n_results=n_results
        )

        # ----------------------------------------------------
        # Extract results
        # ----------------------------------------------------

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        ids = results.get(
            "ids",
            [[]]
        )[0]

        retrieved = []

        for i, document in enumerate(
            documents
        ):

            retrieved.append(
                {
                    "text": document,
                    "metadata": (
                        metadatas[i]
                        if i < len(metadatas)
                        else {}
                    ),
                    "distance": (
                        distances[i]
                        if i < len(distances)
                        else None
                    ),
                    "id": (
                        ids[i]
                        if i < len(ids)
                        else None
                    )
                }
            )

        return retrieved

    # ========================================================
    # RETRIEVE TEXT ONLY
    # ========================================================

    def retrieve_text(
        self,
        query: str,
        n_results: int = 5
    ) -> List[str]:
        """
        Return only retrieved text chunks.
        """

        results = self.retrieve(
            query=query,
            n_results=n_results
        )

        return [
            result["text"]
            for result in results
        ]

    # ========================================================
    # BUILD CONTEXT
    # ========================================================

    def build_context(
        self,
        query: str,
        n_results: int = 5
    ) -> str:
        """
        Combine retrieved chunks into a single
        context string for the RAG LLM.
        """

        results = self.retrieve(
            query=query,
            n_results=n_results
        )

        if not results:
            return ""

        context_parts = []

        for i, result in enumerate(
            results,
            start=1
        ):

            source = result[
                "metadata"
            ].get(
                "source",
                "Unknown"
            )

            source_type = result[
                "metadata"
            ].get(
                "source_type",
                "Unknown"
            )

            context_parts.append(
                f"[Source {i}]\n"
                f"Type: {source_type}\n"
                f"Source: {source}\n"
                f"Content:\n"
                f"{result['text']}"
            )

        return "\n\n".join(
            context_parts
        )