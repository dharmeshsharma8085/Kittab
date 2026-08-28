from document import (
    from_pdf,
    from_audio,
    from_video,
    from_ocr,
    from_web,
    document_info
)


# ============================================================
# DOCUMENT TEST
# ============================================================

print(
    "\nKITTAB DOCUMENT TEST"
)

print(
    "=" * 60
)


# ============================================================
# PDF
# ============================================================

pdf_doc = from_pdf(
    text="This is a sample PDF document.",
    file_path="example.pdf"
)


# ============================================================
# AUDIO
# ============================================================

audio_doc = from_audio(
    text="This is a sample audio transcript.",
    file_path="lecture.mp3"
)


# ============================================================
# VIDEO
# ============================================================

video_doc = from_video(
    text="This is a sample video transcript.",
    video_url="https://youtube.com/example"
)


# ============================================================
# OCR
# ============================================================

ocr_doc = from_ocr(
    text="This is handwritten note text.",
    image_path="notes.jpg"
)


# ============================================================
# WEB
# ============================================================

web_doc = from_web(
    text="This is extracted website content.",
    url="https://example.com",
    title="Example Website"
)


# ============================================================
# DISPLAY
# ============================================================

documents = [
    pdf_doc,
    audio_doc,
    video_doc,
    ocr_doc,
    web_doc
]


for i, document in enumerate(
    documents,
    start=1
):

    print(
        f"\nDocument {i}"
    )

    print(
        "-" * 40
    )

    print(
        document_info(
            document
        )
    )


print(
    "\nDocument layer test completed."
)