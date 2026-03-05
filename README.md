# LexRAG ⚖️

### Multimodal AI System for Court Case Precedent Retrieval

LexRAG is an **AI-powered legal research system** that retrieves relevant court case precedents from legal documents and evidence using **Retrieval-Augmented Generation (RAG)**.

The system supports **multimodal inputs** such as PDFs, scanned documents, and evidence images. It applies advanced retrieval techniques like **Multi-Query expansion**, **HyDE retrieval**, and **Parent–Child indexing** to improve legal search accuracy.

---

# 🚀 Features

* 📄 **Multimodal Document Processing**

  * Upload court case PDFs
  * Upload scanned documents
  * Upload evidence images (OCR supported)

* 🔍 **Advanced Retrieval**

  * Multi-Query expansion
  * HyDE retrieval
  * Semantic vector search

* ⚖️ **Legal Case Analysis**

  * Extract legal principles
  * Identify similar precedents
  * Summarize court reasoning

* 🧠 **RAG-based Answer Generation**

  * Grounded responses using retrieved case context

* 📊 **Evaluation Framework**

  * Precision@K
  * Recall@K
  * Mean Reciprocal Rank (MRR)
  * F1 Score
  * LLM-as-a-Judge evaluation

* 🔐 **Security Layer**

  * Prompt injection protection

---

# 🏗️ Architecture

```
Documents (PDF / Images)
        │
        ▼
Text Extraction (PDF Parser + OCR)
        │
        ▼
Text Cleaning
        │
        ▼
Parent–Child Chunking
        │
        ▼
Embedding Model
(sentence-transformers)
        │
        ▼
Vector Database (ChromaDB)
        │
        ▼
User Query
        │
        ▼
Multi-Query Expansion
        │
        ▼
HyDE Retrieval
        │
        ▼
Vector Similarity Search
        │
        ▼
Top Case Chunks
        │
        ▼
LLM Generation (RAG)
        │
        ▼
AI Legal Analysis
```

---

# 🧠 Key AI Concepts Used

### Retrieval-Augmented Generation (RAG)

Combines vector search with LLM generation to produce **grounded answers**.

### Multi-Query Retrieval

Generates multiple query variations to improve recall.

### HyDE Retrieval

Creates a hypothetical answer and embeds it for improved semantic search.

### Parent–Child Indexing

Legal documents are split into structured sections such as:

* Facts
* Legal Issue
* Arguments
* Reasoning
* Judgment

This improves retrieval precision.

---

# 🛠️ Tech Stack

| Component           | Technology                        |
| ------------------- | --------------------------------- |
| Frontend            | Streamlit                         |
| LLM API             | Groq                              |
| Embeddings          | HuggingFace Sentence Transformers |
| Vector Database     | ChromaDB                          |
| OCR                 | Tesseract                         |
| Backend             | Python                            |
| Retrieval Framework | LangChain                         |

---

# 📂 Project Structure

```
court_precedent_finder/

├── app.py
├── config/
├── ingestion/
│   ├── pdf_parser.py
│   ├── image_processor.py
│   └── citation_extractor.py
├── indexing/
│   ├── chroma_manager.py
│   └── parent_child_indexer.py
├── retrieval/
│   ├── multi_query.py
│   ├── hyde.py
│   ├── hybrid_ranker.py
│   └── answer_builder.py
├── evaluation/
│   ├── metrics.py
│   └── evaluation_dashboard.py
├── security/
│   └── guard.py
└── utils/
```

---

# ⚙️ Installation

### Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/lexrag.git
cd lexrag
```

### Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create `.env` file:

```
GROQ_API_KEY=your_groq_api_key
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

Open:

```
http://localhost:8501
```

---

# 📊 Evaluation

The system supports retrieval evaluation metrics:

| Metric      | Purpose                                |
| ----------- | -------------------------------------- |
| Precision@K | Measures relevant retrieved documents  |
| Recall@K    | Measures if correct document retrieved |
| MRR         | Measures ranking quality               |
| F1 Score    | Balance of precision and recall        |

It also includes **LLM-as-a-Judge evaluation** for assessing answer quality.

---

# 💡 Example Query

```
Explain limits on constitutional amendments in India
```

Output:

* Summary of legal principle
* Relevant precedent cases
* Legal reasoning extracted from judgments

---

# 🎯 Use Cases

* Legal research assistance
* Case precedent discovery
* Legal document analysis
* AI-powered law assistants

---

# 📌 Future Improvements

* Citation graph analysis
* Case relationship visualization
* Automated evaluation datasets
* Legal knowledge graph integration

---

# 👨‍💻 Author

Built as an AI research project exploring **multimodal RAG systems for legal intelligence**.
