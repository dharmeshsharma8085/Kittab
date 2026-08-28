import os

from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)


# ============================================================
# EMBEDDER
# ============================================================

class Embedder:
    """
    Convert text into vector embeddings
    for Kittab's RAG pipeline.
    """

    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL
    ):
        print(
            "\nLoading embedding model..."
        )

        print(
            f"Model: {model_name}"
        )

        try:

            self.model = SentenceTransformer(
                model_name
            )

        except Exception as exc:

            raise RuntimeError(
                "Failed to load embedding model:\n"
                f"{exc}"
            ) from exc

        print(
            "Embedding model loaded successfully."
        )

    # ========================================================
    # EMBED ONE TEXT
    # ========================================================

    def embed_text(
        self,
        text: str
    ) -> list:

        if not isinstance(
            text,
            str
        ):
            raise TypeError(
                "Text must be a string."
            )

        text = text.strip()

        if not text:
            raise ValueError(
                "Text cannot be empty."
            )

        try:

            embedding = self.model.encode(
                text,
                convert_to_numpy=True
            )

        except Exception as exc:

            raise RuntimeError(
                f"Failed to create embedding:\n"
                f"{exc}"
            ) from exc

        return embedding.tolist()

    # ========================================================
    # EMBED MULTIPLE TEXTS
    # ========================================================

    def embed_texts(
        self,
        texts: list
    ) -> list:

        if not texts:

            raise ValueError(
                "Text list cannot be empty."
            )

        cleaned_texts = []

        for text in texts:

            if not isinstance(
                text,
                str
            ):
                raise TypeError(
                    "Every item must be a string."
                )

            text = text.strip()

            if text:
                cleaned_texts.append(
                    text
                )

        if not cleaned_texts:

            raise ValueError(
                "No valid text found."
            )

        try:

            embeddings = self.model.encode(
                cleaned_texts,
                convert_to_numpy=True,
                show_progress_bar=False
            )

        except Exception as exc:

            raise RuntimeError(
                f"Failed to create embeddings:\n"
                f"{exc}"
            ) from exc

        return embeddings.tolist()

    # ========================================================
    # EMBEDDING DIMENSION
    # ========================================================

    def dimension(self) -> int:

        return self.model.get_sentence_embedding_dimension()