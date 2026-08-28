````markdown
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
````

### 📝 Learning Tools

* AI Question Answering
* Test Generation
* Flashcard Generation
* Source-aware responses

---

## 🛠️ Tech Stack

### AI / LLM

* Google Gemini
* Sentence Transformers
* Whisper

### RAG

* ChromaDB
* Vector Embeddings
* Similarity Search
* Retrieval-Augmented Generation

### Document Processing

* PyPDF2
* yt-dlp
* EasyOCR
* Pillow
* Web extraction

### Backend

* Python

### Planned Web Application

* FastAPI
* HTML
* CSS
* JavaScript

---

## 📁 Project Structure

```text
KITTAB/
│
├── AUDIO/
│   ├── extractor.py
│   ├── transcriber.py
│   └── summarize.py
│
├── OCR/
│   ├── ocr_reader.py
│   └── test_ocr.py
│
├── PDF/
│   ├── pdf_loader.py
│   ├── chunker.py
│   └── vector_store.py
│
├── VIDEO/
│   ├── video_loader.py
│   ├── video_audio.py
│   ├── test_video.py
│   └── test_video_audio.py
│
├── WEB/
│   └── web_loader.py
│
├── RAG/
│   ├── document.py
│   ├── embedder.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── rag_engine.py
│   ├── pipeline.py
│   ├── flashcard_generator.py
│   ├── test_generator.py
│   └── test_*.py
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/dharmeshsharma8085/Kittab.git
cd Kittab
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate environment

Windows:

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_gemini_model

MISTRAL_API_KEY=your_mistral_api_key

WHISPER_MODEL=small

SARVAM_API_KEY=your_sarvam_api_key
SARVAM_STT_MODEL=saaras:v3
```

**Never commit your `.env` file or API keys to GitHub.**

---

## 🧪 Current Development Status

| Component                | Status |
| ------------------------ | ------ |
| PDF Loader               | ✅      |
| Audio Processing         | ✅      |
| Video Loader             | ✅      |
| OCR                      | ✅      |
| Web Loader               | ✅      |
| Document Layer           | ✅      |
| Embeddings               | ✅      |
| ChromaDB                 | ✅      |
| Retriever                | ✅      |
| RAG Engine               | ✅      |
| RAG Pipeline             | ✅      |
| Test Generator           | ✅      |
| Flashcard Generator      | ✅      |
| Multi-source Integration | 🔄     |
| Backend API              | 🔜     |
| Web Frontend             | 🔜     |
| Deployment               | 🔜     |

---

## 🧠 Why Kittab?

Students learn from many different sources:

* Lecture recordings
* YouTube videos
* PDFs
* Websites
* Handwritten notes

Kittab brings these sources into one learning system and allows students to interact with their own study material using AI.

---

## 🗺️ Roadmap

### Phase 1 — Core AI

* [x] Multimodal content extraction
* [x] Document processing
* [x] Embeddings
* [x] Vector database
* [x] Retrieval
* [x] RAG
* [x] Test generation
* [x] Flashcards

### Phase 2 — Integration

* [ ] Connect all loaders to the final pipeline
* [ ] Multi-source ingestion
* [ ] Better source tracking
* [ ] Improved error handling

### Phase 3 — Web Application

* [ ] FastAPI backend
* [ ] Custom frontend
* [ ] File upload
* [ ] URL input
* [ ] AI chat
* [ ] Test generation UI
* [ ] Flashcard UI

### Phase 4 — Deployment

* [ ] Production configuration
* [ ] Cloud deployment
* [ ] Public URL
* [ ] Performance optimization
* [ ] Final testing

---

## 📸 Architecture

Kittab's architecture is designed around a simple idea:

```text
         USER
          ↓
   Study Material
          ↓
   Content Extraction
          ↓
      RAG Pipeline
          ↓
     Vector Search
          ↓
      AI Response
          ↓
   Learn / Test / Revise
```

---

## 👨‍💻 Author

**Dharmesh Sharma**

AI/ML & Generative AI Developer

Building Kittab to explore practical applications of:

* Machine Learning
* Generative AI
* LLMs
* RAG
* Multimodal AI
* AI Agents

---

## ⭐ Support

If you find Kittab interesting, consider giving the repository a ⭐ on GitHub.

More features are coming soon.

---

## 📌 Project Status

Kittab is currently under active development.

The core AI and RAG components are being built first, followed by the complete web application and public deployment.

```
```
