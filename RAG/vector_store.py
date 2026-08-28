import uuid
from typing import List, Dict, Optional

import chromadb


# ============================================================
# CONFIGURATION
# ============================================================

COLLECTION_NAME = "kittab_documents"

CHROMA_PATH = "./chroma_db"


# ============================================================
# VECTOR STORE
# ============================================================

class VectorStore:
    """
    ChromaDB vector store for Kittab RAG.
    """

    def __init__(
        self,
        collection_name: str = COLLECTION_NAME,
        persist_directory: str = CHROMA_PATH
    ):
        print(
            "\nInitializing ChromaDB..."
        )

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )

        print(
            "ChromaDB initialized successfully."
        )

        print(
            f"Collection: {collection_name}"
        )

    # ========================================================
    # ADD DOCUMENTS
    # ========================================================

    def add_documents(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ) -> None:
        """
        Add multiple text chunks and their embeddings
        to ChromaDB.
        """

        if not texts:

            raise ValueError(
                "Texts cannot be empty."
            )

        if not embeddings:

            raise ValueError(
                "Embeddings cannot be empty."
            )

        if len(texts) != len(embeddings):

            raise ValueError(
                "Number of texts and embeddings "
                "must be the same."
            )

        # ----------------------------------------------------
        # Generate IDs
        # ----------------------------------------------------

        if ids is None:

            ids = [
                str(uuid.uuid4())
                for _ in texts
            ]

        if len(ids) != len(texts):

            raise ValueError(
                "Number of IDs must match "
                "number of texts."
            )

        # ----------------------------------------------------
        # Metadata
        # ----------------------------------------------------

        if metadatas is None:

            metadatas = [
                {}
                for _ in texts
            ]

        if len(metadatas) != len(texts):

            raise ValueError(
                "Number of metadatas must match "
                "number of texts."
            )

        # ----------------------------------------------------
        # Validate documents
        # ----------------------------------------------------

        valid_texts = []
        valid_embeddings = []
        valid_metadatas = []
        valid_ids = []

        for text, embedding, metadata, doc_id in zip(
            texts,
            embeddings,
            metadatas,
            ids
        ):

            if not isinstance(
                text,
                str
            ):
                continue

            text = text.strip()

            if not text:
                continue

            valid_texts.append(
                text
            )

            valid_embeddings.append(
                embedding
            )

            valid_metadatas.append(
                metadata
            )

            valid_ids.append(
                doc_id
            )

        # ----------------------------------------------------
        # Check valid documents
        # ----------------------------------------------------

        if not valid_texts:

            raise ValueError(
                "No valid documents to add."
            )

        # ----------------------------------------------------
        # Add to ChromaDB
        # ----------------------------------------------------

        try:

            self.collection.add(
                ids=valid_ids,
                documents=valid_texts,
                embeddings=valid_embeddings,
                metadatas=valid_metadatas
            )

        except Exception as exc:

            raise RuntimeError(
                "Failed to add documents "
                f"to ChromaDB:\n{exc}"
            ) from exc

        print(
            f"Added {len(valid_texts)} "
            f"documents to ChromaDB."
        )

    # ========================================================
    # SEARCH
    # ========================================================

    def search(
        self,
        query_embedding: List[float],
        n_results: int = 5
    ) -> Dict:
        """
        Search ChromaDB using a query embedding.
        """

        if not query_embedding:

            raise ValueError(
                "Query embedding cannot be empty."
            )

        if n_results < 1:

            raise ValueError(
                "n_results must be at least 1."
            )

        try:

            results = self.collection.query(
                query_embeddings=[
                    query_embedding
                ],
                n_results=n_results
            )

        except Exception as exc:

            raise RuntimeError(
                "ChromaDB search failed:\n"
                f"{exc}"
            ) from exc

        return results

    # ========================================================
    # COUNT
    # ========================================================

    def count(self) -> int:
        """
        Return the number of stored documents.
        """

        return self.collection.count()

    # ========================================================
    # CLEAR COLLECTION
    # ========================================================

    def clear(self) -> None:
        """
        Delete all documents from the collection.
        """

        try:

            collection_name = (
                self.collection.name
            )

            self.client.delete_collection(
                collection_name
            )

            self.collection = (
                self.client.get_or_create_collection(
                    name=collection_name
                )
            )

        except Exception as exc:

            raise RuntimeError(
                "Failed to clear ChromaDB:\n"
                f"{exc}"
            ) from exc

        print(
            "ChromaDB collection cleared."
        )