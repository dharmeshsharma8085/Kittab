from pathlib import Path
import sys


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(r"C:\KITTAB")

PDF_LOADER_FOLDER = BASE_DIR / "PDF"

PDF_PATH = Path(
    r"C:\Users\DHARMESH SHARMA\Downloads\DSA_for_AI_Engineers.pdf"
)


# ============================================================
# IMPORT PDF LOADER
# ============================================================

if not PDF_LOADER_FOLDER.exists():

    raise FileNotFoundError(
        f"""
PDF loader folder not found:

{PDF_LOADER_FOLDER}
"""
    )


if str(PDF_LOADER_FOLDER) not in sys.path:

    sys.path.insert(
        0,
        str(PDF_LOADER_FOLDER)
    )


try:

    from pdf_loader import extract_text_from_pdf

except ImportError as exc:

    raise ImportError(
        f"""
Could not import PDF loader.

Expected file:

{PDF_LOADER_FOLDER / "pdf_loader.py"}

Required function:

extract_text_from_pdf()

Original error:

{exc}
"""
    ) from exc


# ============================================================
# IMPORT RAG COMPONENTS
# ============================================================

try:

    from pipeline import RAGPipeline
    from retriever import Retriever
    from rag_engine import RAGEngine

except ImportError as exc:

    raise ImportError(
        f"""
Could not import RAG components.

Expected folder:

{BASE_DIR / "RAG"}

Required files:

- pipeline.py
- retriever.py
- rag_engine.py

Original error:

{exc}
"""
    ) from exc


# ============================================================
# START
# ============================================================

print(
    "\nKITTAB REAL PDF → RAG TEST"
)

print(
    "=" * 60
)


# ============================================================
# CHECK PDF
# ============================================================

print(
    "\nChecking PDF..."
)

print(
    f"Path:\n{PDF_PATH}"
)


if not PDF_PATH.exists():

    raise FileNotFoundError(
        f"""
PDF not found:

{PDF_PATH}
"""
    )


if not PDF_PATH.is_file():

    raise ValueError(
        f"""
PDF path is not a file:

{PDF_PATH}
"""
    )


if PDF_PATH.suffix.lower() != ".pdf":

    raise ValueError(
        f"""
File must be a PDF:

{PDF_PATH}
"""
    )


print(
    "PDF found successfully."
)


# ============================================================
# PDF INFORMATION
# ============================================================

print(
    "\nPDF INFORMATION"
)

print(
    "-" * 60
)

print(
    f"File: {PDF_PATH.name}"
)

print(
    f"Size: {PDF_PATH.stat().st_size:,} bytes"
)


# ============================================================
# LOAD PDF
# ============================================================

print(
    "\nLoading PDF..."
)

try:

    text = extract_text_from_pdf(
        str(PDF_PATH)
    )

except Exception as exc:

    print(
        "\n❌ PDF EXTRACTION FAILED"
    )

    print(
        "=" * 60
    )

    print(
        exc
    )

    raise SystemExit(1)


# ============================================================
# VALIDATE TEXT
# ============================================================

if text is None:

    raise RuntimeError(
        "PDF loader returned None."
    )


if not text.strip():

    raise RuntimeError(
        """
PDF extraction returned empty text.

Possible reasons:

- scanned PDF
- image-only PDF
- protected PDF
- no selectable text
"""
    )


print(
    "\nPDF extraction successful."
)

print(
    f"Extracted characters: {len(text):,}"
)


# ============================================================
# TEXT PREVIEW
# ============================================================

print(
    "\nTEXT PREVIEW"
)

print(
    "-" * 60
)

print(
    text[:1000]
)

if len(text) > 1000:

    print(
        "\n...[preview truncated]"
    )


# ============================================================
# CREATE RAG PIPELINE
# ============================================================

print(
    "\nCreating RAG Pipeline..."
)

try:

    pipeline = RAGPipeline()

except Exception as exc:

    print(
        "\n❌ PIPELINE INITIALIZATION FAILED"
    )

    print(
        "=" * 60
    )

    print(
        exc
    )

    raise SystemExit(1)


print(
    "RAG Pipeline initialized successfully."
)


# ============================================================
# CHECK VECTOR STORE API
# ============================================================

print(
    "\nChecking VectorStore..."
)

if not hasattr(
    pipeline.vector_store,
    "add_documents"
):

    print(
        "\n❌ VectorStore API ERROR"
    )

    print(
        "=" * 60
    )

    print(
        "Expected method:"
    )

    print(
        "add_documents()"
    )

    print(
        "\nAvailable methods:"
    )

    print(
        [
            name
            for name in dir(
                pipeline.vector_store
            )
            if not name.startswith("_")
        ]
    )

    raise SystemExit(1)


print(
    "VectorStore.add_documents() found."
)


# ============================================================
# INGEST PDF
# ============================================================

print(
    "\nSending PDF to RAG pipeline..."
)

try:

    ingestion_result = pipeline.ingest_text(

        text=text,

        source_type="pdf",

        source=str(PDF_PATH),

        metadata={
            "filename": PDF_PATH.name
        }
    )

except Exception as exc:

    print(
        "\n❌ PDF INGESTION FAILED"
    )

    print(
        "=" * 60
    )

    print(
        exc
    )

    raise SystemExit(1)


# ============================================================
# INGESTION RESULT
# ============================================================

print(
    "\nINGESTION RESULT"
)

print(
    "=" * 60
)

print(
    f"Source: "
    f"{ingestion_result.get('source')}"
)

print(
    f"Characters: "
    f"{ingestion_result.get('characters', 0):,}"
)

print(
    f"Chunks: "
    f"{ingestion_result.get('chunks', 0)}"
)

print(
    f"Embeddings: "
    f"{ingestion_result.get('embeddings', 0)}"
)


# ============================================================
# CHROMADB COUNT
# ============================================================

print(
    "\nCHROMADB"
)

print(
    "-" * 60
)

try:

    stored_chunks = pipeline.count()

except Exception as exc:

    print(
        "\n❌ CHROMADB COUNT FAILED"
    )

    print(
        exc
    )

    raise SystemExit(1)


print(
    f"Stored chunks: {stored_chunks}"
)


# ============================================================
# CREATE RETRIEVER
# ============================================================

print(
    "\nInitializing Retriever..."
)

try:

    retriever = Retriever(

        embedder=pipeline.embedder,

        vector_store=pipeline.vector_store
    )

except Exception as exc:

    print(
        "\n❌ RETRIEVER INITIALIZATION FAILED"
    )

    print(
        "=" * 60
    )

    print(
        exc
    )

    raise SystemExit(1)


print(
    "Retriever initialized successfully."
)


# ============================================================
# CREATE RAG ENGINE
# ============================================================

print(
    "\nInitializing RAG Engine..."
)

try:

    rag = RAGEngine(

        retriever=retriever,

        top_k=5
    )

except Exception as exc:

    print(
        "\n❌ RAG ENGINE INITIALIZATION FAILED"
    )

    print(
        "=" * 60
    )

    print(
        exc
    )

    raise SystemExit(1)


print(
    "RAG Engine initialized successfully."
)


# ============================================================
# QUESTION
# ============================================================

print(
    "\n"
    + "=" * 60
)

question = input(
    "Ask something about the PDF: "
).strip()


if not question:

    raise ValueError(
        "Question cannot be empty."
    )


# ============================================================
# GENERATE ANSWER
# ============================================================

print(
    "\nGenerating answer..."
)

try:

    result = rag.ask_with_sources(
        question
    )

except Exception as exc:

    print(
        "\n❌ RAG GENERATION FAILED"
    )

    print(
        "=" * 60
    )

    print(
        exc
    )

    error_text = str(exc).lower()

    if (
        "503" in error_text
        or "unavailable" in error_text
        or "high demand" in error_text
    ):

        print(
            "\n⚠️ Gemini is temporarily unavailable."
        )

        print(
            "PDF extraction, chunking, embeddings, "
            "ChromaDB and retrieval were initialized."
        )

    raise SystemExit(1)


# ============================================================
# ANSWER
# ============================================================

print(
    "\nANSWER"
)

print(
    "=" * 60
)

answer = result.get(
    "answer",
    ""
)


if answer:

    print(
        answer
    )

else:

    print(
        "No answer returned."
    )


# ============================================================
# SOURCES
# ============================================================

print(
    "\nSOURCES"
)

print(
    "=" * 60
)

sources = result.get(
    "sources",
    []
)


if not sources:

    print(
        "No sources returned."
    )

else:

    for index, source in enumerate(
        sources,
        start=1
    ):

        print(
            f"\nSource {index}"
        )

        print(
            f"Type: "
            f"{source.get('source_type', 'Unknown')}"
        )

        print(
            f"Source: "
            f"{source.get('source', 'Unknown')}"
        )

        if source.get("distance") is not None:

            print(
                f"Distance: "
                f"{source.get('distance')}"
            )


# ============================================================
# COMPLETE
# ============================================================

print(
    "\n"
    + "=" * 60
)

print(
    "REAL PDF → RAG TEST COMPLETED ✅"
)

print(
    "=" * 60
)