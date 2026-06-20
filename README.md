# CloudSync Pro Support System

## 📖 Overview

A **premium, AI‑driven customer support dispatcher** built with **Streamlit**, **FAISS** for semantic retrieval, and **LangChain** agents for classification and escalation.  The app enables users to:
- Chat with an autonomous AI that classifies the request (Technical, Frustrated, Executive, or None).
- Retrieve relevant documentation chunks from a local FAISS index.
- Automatically trigger escalation policies and provide a hand‑off summary when needed.

The UI follows a dark glass‑morphism design with vibrant gradients, custom persona badges, and a diagnostics panel.

---

## ✨ Features

- **Real‑time chat UI** powered by Streamlit.
- **Zero‑shot persona classification** using a lightweight LLM.
- **FAISS vector store** for fast semantic document retrieval.
- **Escalation workflow** (auto‑hand‑off JSON summary).
- **Dynamic diagnostics panel** showing persona, similarity score, retrieved docs, and escalation status.
- **Environment‑based configuration** via `python‑dotenv`.

---

## 🏗️ Architecture

```
cloudsync-pro-support/
│   app.py               # Streamlit entry point
│   .env                 # Environment variables (ignored by git)
│   requirements.txt     # Python dependencies
│
└───src/
    │   agent.py          # Core LLM orchestration & classification
    │   config.py         # Config helpers (FAISS index, model settings)
    │   database.py       # Optional persistence layer
    │   ...
```

---

## ⚙️ Installation

```bash
# Clone the repo (once it exists on GitHub)
git clone https://github.com/Arpit-kale/cloudsync-pro-support.git
cd cloudsync-pro-support

# Create a virtual environment
python -m venv .venv
.venv\Scripts\activate   # PowerShell: .venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create a .env file (see below) and add your API keys
```

---

## 📦 Usage

```bash
# Start the Streamlit app
streamlit run app.py
```

Open your browser at `http://localhost:8501`.  The chat interface will load automatically.

---

## 🔐 Environment Variables (`.env`)

| Variable | Description |
|----------|-------------|
| `API_KEY` | **CloudSync Pro API key** – used by the agent to look up internal resources. |
| `FAISS_INDEX_PATH` | Path to the FAISS index (default `./data/faiss_index`). |
| `OPENAI_API_KEY` | OpenAI secret key for LLM inference. |

> **Never commit** `.env` to version control – it is listed in `.gitignore`.

---

## 📸 Demo Screenshot

*(Replace the placeholder with an actual screenshot later.)*

![Demo Screenshot](./assets/demo.png)

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/awesome-feature`.
3. Make your changes and ensure the app runs locally.
4. Open a Pull Request with a clear description of the changes.

---

## 📄 License

This project is licensed under the **MIT License** – see `LICENSE` for details.

---
