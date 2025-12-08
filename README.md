# Knowledge-Based RAG Engine (Gemini + ChromaDB)

A lightweight Retrieval-Augmented Generation (RAG) system that lets you upload
documents (PDF, DOCX, TXT, images) and ask questions about them using Google
Gemini models. The system extracts text, embeds it using Gemini embeddings,
stores vectors in ChromaDB, retrieves relevant chunks, and generates an answer
using Gemini 2.0 Flash.

This project is designed to be simple, fast, and easy to extend.

---

## 🚀 Features

- Upload PDFs, DOCX, TXT, and Images
- Text extraction + OCR fallback (pdfplumber + Tesseract)
- Chunking and metadata storage
- Gemini-powered embeddings (text-embedding-004)
- ChromaDB vector store (persistent)
- RAG pipeline with Gemini Flash for answer generation
- Clean frontend UI (HTML + JS)
- Fully CORS-enabled backend (FastAPI)
- Works entirely locally (except Gemini API calls)

---

## 🧩 Tech Stack

### **Backend**
- Python 3.10
- FastAPI
- ChromaDB (Persistent DB)
- Google Generative AI (Gemini APIs)
- pdfplumber (PDF extraction)
- pytesseract + pdf2image (OCR fallback)
- DOCX parser
- Uvicorn server

### **Frontend**
- HTML / CSS / JavaScript
- Modern, clean minimalistic interface
- AJAX file upload + query system
- Displays answer and sources

---

## 📁 Project Structure

knowledge-based-rag/
│
├── backend/
│ ├── app.py # FastAPI server + routes
│ ├── embeddings.py # Gemini embedding functions
│ ├── vector_store.py # ChromaDB setup + CRUD
│ ├── rag_pipeline.py # Extraction, chunking, ingestion
│ ├── llm_client.py # Gemini answer synthesis
│
├── frontend/
│ ├── index.html # Main UI
│
├── data/
│ ├── docs/ # Uploaded documents
│ ├── vectorstore/ # ChromaDB persistent DB
│
└── README.md

yaml
Copy code

---

## ⚙️ Installation & Setup

### 1️⃣ **Install Python 3.10**  
Your system must use **Python 3.10** because newer Python versions break several dependencies.

### 2️⃣ Create a virtual environment
cd knowledge-based-rag
python -m venv .venv

makefile
Copy code

Activate:

Windows (PowerShell):
.venv\Scripts\activate

shell
Copy code

### 3️⃣ Install dependencies
pip install -r requirements.txt

markdown
Copy code

### 4️⃣ Install Tesseract (for image-only PDFs)
Windows:
- Download: https://github.com/UB-Mannheim/tesseract/wiki
- Install
- Add to PATH:
C:\Program Files\Tesseract-OCR\

makefile
Copy code

Verify:
tesseract --version

makefile
Copy code

### 5️⃣ Set your Gemini API key
PowerShell:
setx GEMINI_API_KEY "YOUR_KEY"

sql
Copy code

OR create `.env` with:
GEMINI_API_KEY=YOUR_KEY

yaml
Copy code

---

## ▶️ Run Backend

uvicorn backend.app:app --reload

nginx
Copy code

Backend runs on:
http://127.0.0.1:8000

yaml
Copy code

---

## ▶️ Run Frontend

cd frontend
python -m http.server 5500

makefile
Copy code

Visit:
http://127.0.0.1:5500/index.html

yaml
Copy code

---

## 🧪 Usage Flow

### 1. Upload Document  
Click **Upload**, select a PDF/DOCX/TXT/Image → backend extracts text → chunks → embeds → stores.

### 2. Ask a Question  
Enter query → backend retrieves relevant chunks → Gemini generates final answer.

### 3. See Output  
UI shows:
- Final Answer
- Sources (file + chunk index)
- Extracted text snippet

---

## 🔥 Notes

- Works well with real-world messy PDFs.
- Supports OCR auto fallback for scanned/image-only files.
- ChromaDB persists vectors automatically.
- Fully stateless — restart server without losing data.

---

## 🧩 Future Improvements
- Support multiple collection namespaces
- Add UI for viewing ingested documents
- Add PDF preview before ingestion
- Add Docker support

---

## 🏁 License
MIT License