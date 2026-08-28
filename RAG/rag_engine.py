import os

from dotenv import load_dotenv
from google import genai

from retriever import Retriever


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.7-flash"
)

if not GEMINI_API_KEY:

    raise RuntimeError(
        "GEMINI_API_KEY is not set in .env"
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# RAG ENGINE
# ============================================================

class RAGEngine:
    """
    Kittab Retrieval-Augmented Generation engine.

    Retrieves relevant information from ChromaDB
    and uses Gemini to generate a grounded answer.
    """

    def __init__(
        self,
        retriever: Retriever = None,
        top_k: int = 5
    ):

        print(
            "\nInitializing RAG Engine..."
        )

        self.retriever = (
            retriever
            if retriever is not None
            else Retriever()
        )

        self.top_k = top_k

        print(
            f"Top-K retrieval: {self.top_k}"
        )

        print(
            f"Gemini model: {GEMINI_MODEL}"
        )

        print(
            "RAG Engine initialized successfully."
        )

    # ========================================================
    # BUILD PROMPT
    # ========================================================

    def _build_prompt(
        self,
        query: str,
        context: str
    ) -> str:

        return f"""
You are Kittab, an AI study assistant.

Answer the user's question using ONLY
the provided context.

IMPORTANT RULES:

1. Use the provided context as the primary source.

2. Do not invent facts that are not present
   in the context.

3. If the answer cannot be found in the context,
   clearly say:
   "I couldn't find this information in the
   provided material."

4. Explain the answer clearly and simply.

5. For technical questions, include useful
   details from the context.

6. If the context contains multiple sources,
   combine them when relevant.

7. Do not mention internal retrieval,
   embeddings, vectors, or ChromaDB unless
   the user specifically asks about them.

8. Do not pretend to know something that
   is absent from the provided material.

9. Keep the answer focused on the user's question.

------------------------------------------------------------
CONTEXT
------------------------------------------------------------

{context}

------------------------------------------------------------
USER QUESTION
------------------------------------------------------------

{query}

------------------------------------------------------------

Answer the question now.
"""

    # ========================================================
    # ASK
    # ========================================================

    def ask(
        self,
        query: str
    ) -> str:
        """
        Retrieve relevant context and generate
        a grounded answer.
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

        print(
            "\nRetrieving relevant information..."
        )

        # ----------------------------------------------------
        # Retrieve
        # ----------------------------------------------------

        context = self.retriever.build_context(
            query=query,
            n_results=self.top_k
        )

        # ----------------------------------------------------
        # No context
        # ----------------------------------------------------

        if not context.strip():

            return (
                "I couldn't find this information "
                "in the provided material."
            )

        print(
            "Relevant context retrieved."
        )

        # ----------------------------------------------------
        # Build prompt
        # ----------------------------------------------------

        prompt = self._build_prompt(
            query=query,
            context=context
        )

        # ----------------------------------------------------
        # Generate answer
        # ----------------------------------------------------

        print(
            "Generating answer with Gemini..."
        )

        try:

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

        except Exception as exc:

            raise RuntimeError(
                f"Gemini generation failed:\n"
                f"{exc}"
            ) from exc

        # ----------------------------------------------------
        # Validate response
        # ----------------------------------------------------

        if not response.text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        answer = response.text.strip()

        print(
            "Answer generated successfully."
        )

        return answer

    # ========================================================
    # ASK WITH SOURCES
    # ========================================================

    def ask_with_sources(
        self,
        query: str
    ) -> dict:
        """
        Return answer together with retrieved sources.
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

        # ----------------------------------------------------
        # Retrieve documents directly
        # ----------------------------------------------------

        results = self.retriever.retrieve(
            query=query,
            n_results=self.top_k
        )

        if not results:

            return {
                "answer": (
                    "I couldn't find this information "
                    "in the provided material."
                ),
                "sources": []
            }

        # ----------------------------------------------------
        # Build context
        # ----------------------------------------------------

        context_parts = []

        sources = []

        for i, result in enumerate(
            results,
            start=1
        ):

            metadata = result.get(
                "metadata",
                {}
            )

            context_parts.append(
                f"[Source {i}]\n"
                f"{result['text']}"
            )

            sources.append(
                {
                    "id": result.get("id"),
                    "source": metadata.get(
                        "source",
                        "Unknown"
                    ),
                    "source_type": metadata.get(
                        "source_type",
                        "Unknown"
                    ),
                    "distance": result.get(
                        "distance"
                    )
                }
            )

        context = "\n\n".join(
            context_parts
        )

        # ----------------------------------------------------
        # Generate answer
        # ----------------------------------------------------

        prompt = self._build_prompt(
            query=query,
            context=context
        )

        try:

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

        except Exception as exc:

            raise RuntimeError(
                f"Gemini generation failed:\n"
                f"{exc}"
            ) from exc

        if not response.text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return {
            "answer": response.text.strip(),
            "sources": sources
        }