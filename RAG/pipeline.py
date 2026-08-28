from typing import Dict, List, Optional

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from document import create_document
from embedder import Embedder
from vector_store import VectorStore


# ============================================================
# CONFIGURATION
# ============================================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


# ============================================================
# KITTAB RAG PIPELINE
# ============================================================

class RAGPipeline:
    """
    Main ingestion pipeline for Kittab.

    Extracted text
        ↓
    Document
        ↓
    Chunks
        ↓
    Embeddings
        ↓
    ChromaDB
    """

    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
        embedder: Optional[Embedder] = None,
        vector_store: Optional[VectorStore] = None
    ):

        print(
            "\nInitializing Kittab RAG Pipeline..."
        )

        # ----------------------------------------------------
        # Validate chunk settings
        # ----------------------------------------------------

        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than 0."
            )

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap cannot be negative."
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # ----------------------------------------------------
        # Text splitter
        # ----------------------------------------------------

        self.splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=[
                    "\n\n",
                    "\n",
                    ". ",
                    " ",
                    ""
                ]
            )
        )

        # ----------------------------------------------------
        # Embedder
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
            "RAG Pipeline initialized successfully."
        )

    # ========================================================
    # CREATE DOCUMENT
    # ========================================================

    def create_document(
        self,
        text: str,
        source_type: str,
        source: str,
        metadata: Optional[Dict] = None
    ):
        """
        Convert extracted content into
        Kittab's standard Document.
        """

        return create_document(
            text=text,
            source_type=source_type,
            source=source,
            metadata=metadata
        )

    # ========================================================
    # CHUNK DOCUMENT
    # ========================================================

    def chunk_document(
        self,
        document
    ) -> List[str]:
        """
        Split a Document into smaller chunks.
        """

        if not document.text.strip():

            raise ValueError(
                "Document text cannot be empty."
            )

        chunks = self.splitter.split_text(
            document.text
        )

        if not chunks:

            raise RuntimeError(
                "No chunks were created."
            )

        return chunks

    # ========================================================
    # BUILD CHUNK METADATA
    # ========================================================

    def _build_metadata(
        self,
        document,
        chunk_index: int
    ) -> Dict:
        """
        Create metadata for every chunk.
        """

        metadata = dict(
            document.metadata
        )

        metadata.update(
            {
                "source_type": document.source_type,
                "source": document.source,
                "chunk_index": chunk_index
            }
        )

        return metadata

    # ========================================================
    # INGEST DOCUMENT
    # ========================================================

    def ingest_document(
        self,
        document
    ) -> Dict:
        """
        Chunk, embed and store one Document.
        """

        print(
            "\n"
            + "=" * 60
        )

        print(
            "INGESTING DOCUMENT"
        )

        print(
            "=" * 60
        )

        print(
            f"Source type: "
            f"{document.source_type}"
        )

        print(
            f"Source: "
            f"{document.source}"
        )

        print(
            f"Characters: "
            f"{len(document.text):,}"
        )

        # ----------------------------------------------------
        # Chunk
        # ----------------------------------------------------

        print(
            "\nCreating chunks..."
        )

        chunks = self.chunk_document(
            document
        )

        print(
            f"Created {len(chunks)} chunks."
        )

        # ----------------------------------------------------
        # Embeddings
        # ----------------------------------------------------

        print(
            "\nCreating embeddings..."
        )

        embeddings = self.embedder.embed_texts(
            chunks
        )

        print(
            f"Created {len(embeddings)} embeddings."
        )

        # ----------------------------------------------------
        # Metadata
        # ----------------------------------------------------

        metadatas = []

        for index in range(
            len(chunks)
        ):

            metadatas.append(
                self._build_metadata(
                    document,
                    index
                )
            )

        # ----------------------------------------------------
        # Store
        # ----------------------------------------------------

        print(
            "\nAdding chunks to ChromaDB..."
        )

        self.vector_store.add_documents(
            texts=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(
            "\nDocument ingestion completed."
        )

        return {
            "source_type": document.source_type,
            "source": document.source,
            "characters": len(document.text),
            "chunks": len(chunks),
            "embeddings": len(embeddings)
        }

    # ========================================================
    # INGEST TEXT
    # ========================================================

    def ingest_text(
        self,
        text: str,
        source_type: str,
        source: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Complete pipeline for raw extracted text.

        This is the main method that loaders will use.
        """

        document = self.create_document(
            text=text,
            source_type=source_type,
            source=source,
            metadata=metadata
        )

        return self.ingest_document(
            document
        )

    # ========================================================
    # INGEST MULTIPLE DOCUMENTS
    # ========================================================

    def ingest_documents(
        self,
        documents: List
    ) -> List[Dict]:
        """
        Ingest multiple Documents.
        """

        if not documents:

            raise ValueError(
                "Document list cannot be empty."
            )

        results = []

        for index, document in enumerate(
            documents,
            start=1
        ):

            print(
                f"\nProcessing document "
                f"{index}/{len(documents)}..."
            )

            result = self.ingest_document(
                document
            )

            results.append(
                result
            )

        return results

    # ========================================================
    # STORE COUNT
    # ========================================================

    def count(self) -> int:
        """
        Return total chunks currently stored.
        """

        return self.vector_store.count()