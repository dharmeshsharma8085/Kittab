# Kittab 📚

> AI-powered learning assistant that turns your study material into an interactive learning experience.

Kittab is a multimodal AI learning assistant designed to work with different types of study material such as PDFs, audio, videos, handwritten notes, websites, and YouTube content.

The goal is simple:

**Give Kittab your study material → ask questions → learn from your own content.**

---

## 🚀 Features

### 📄 PDF Learning
- Extract text from PDF documents
- Split content into meaningful chunks
- Store document knowledge for retrieval

### 🎵 Audio Learning
- Convert audio into text using speech-to-text
- Process transcripts through the RAG pipeline

### 🎥 Video Learning
- Download YouTube videos
- Extract audio
- Convert video content into text
- Send the extracted content to the RAG pipeline

### ✍️ Handwritten Notes
- OCR support for handwritten notes
- Gemini Vision-based transcription
- Converts handwritten content into structured text

### 🌐 Web Learning
- Extract content from website URLs
- Clean and process website text
- Use web content as a knowledge source

### 🧠 RAG System
Kittab uses Retrieval-Augmented Generation to answer questions using the user's own learning material.

Pipeline:

```text
PDF / Audio / Video / OCR / Web / YouTube
                    ↓
              Text Extraction
                    ↓
              Document Layer
                    ↓
                 Chunking
                    ↓
               Embeddings
                    ↓
                ChromaDB
                    ↓
                Retriever
                    ↓
                RAG Engine
                    ↓
                 Gemini
                    ↓
              AI Answer
