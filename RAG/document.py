from dataclasses import dataclass, field
from typing import Dict, Optional


# ============================================================
# DOCUMENT
# ============================================================

@dataclass
class Document:
    """
    Common document structure used by Kittab RAG.

    Every input source will eventually be converted
    into this format.
    """

    text: str

    source_type: str

    source: str

    metadata: Dict = field(
        default_factory=dict
    )


# ============================================================
# CREATE DOCUMENT
# ============================================================

def create_document(
    text: str,
    source_type: str,
    source: str,
    metadata: Optional[Dict] = None
) -> Document:
    """
    Create a standardized Kittab Document.
    """

    if not isinstance(
        text,
        str
    ):
        raise TypeError(
            "Document text must be a string."
        )

    text = text.strip()

    if not text:
        raise ValueError(
            "Document text cannot be empty."
        )

    if not source_type:
        raise ValueError(
            "source_type cannot be empty."
        )

    if not source:
        raise ValueError(
            "source cannot be empty."
        )

    return Document(
        text=text,
        source_type=source_type,
        source=source,
        metadata=metadata or {}
    )


# ============================================================
# SOURCE-SPECIFIC HELPERS
# ============================================================

def from_pdf(
    text: str,
    file_path: str,
    metadata: Optional[Dict] = None
) -> Document:
    """
    Create a document from a PDF.
    """

    return create_document(
        text=text,
        source_type="pdf",
        source=file_path,
        metadata=metadata
    )


def from_audio(
    text: str,
    file_path: str,
    metadata: Optional[Dict] = None
) -> Document:
    """
    Create a document from an audio transcript.
    """

    return create_document(
        text=text,
        source_type="audio",
        source=file_path,
        metadata=metadata
    )


def from_video(
    text: str,
    video_url: str,
    metadata: Optional[Dict] = None
) -> Document:
    """
    Create a document from a video transcript.
    """

    return create_document(
        text=text,
        source_type="video",
        source=video_url,
        metadata=metadata
    )


def from_ocr(
    text: str,
    image_path: str,
    metadata: Optional[Dict] = None
) -> Document:
    """
    Create a document from handwritten OCR.
    """

    return create_document(
        text=text,
        source_type="ocr",
        source=image_path,
        metadata=metadata
    )


def from_web(
    text: str,
    url: str,
    title: str = "",
    metadata: Optional[Dict] = None
) -> Document:
    """
    Create a document from a website.
    """

    document_metadata = {
        "title": title
    }

    if metadata:
        document_metadata.update(
            metadata
        )

    return create_document(
        text=text,
        source_type="web",
        source=url,
        metadata=document_metadata
    )


# ============================================================
# DOCUMENT PREVIEW
# ============================================================

def document_info(
    document: Document
) -> Dict:
    """
    Return useful information about a document.
    """

    return {
        "source_type": document.source_type,
        "source": document.source,
        "characters": len(
            document.text
        ),
        "metadata": document.metadata
    }