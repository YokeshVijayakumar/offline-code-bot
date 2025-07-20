\# 💻 Offline Code Generator Bot (RAG-Powered)



This is an offline, Streamlit-based coding assistant that generates code using your custom coding style. It uses Retrieval-Augmented Generation (RAG) with CodeLlama and SentenceTransformers.



---

\## ✨ Features



\-   ✅ Code generation using \[CodeLlama](https://ollama.com/library/codellama) via Ollama

\-   🔁 Retrieval of stylistically similar code from your own codebase

\-   📂 Option to upload files for code context

\-   🧠 Embedding-based retrieval with BAAI/bge-small-en-v1.5

\-   🚫 Fully offline — no cloud or internet required



---

\## 🗂 Project Structure



offline-code-bot/

│

├── app.py                   # Streamlit app

├── requirements.txt         # Dependencies

├── README.md                # Project overview

├── .gitignore               # Ignore unnecessary files

│

├── my\_style/                # Your code examples for RAG

├── models/                  # Local embedding model (ignored in Git)

├── models/README.md         # Instructions to download model

└── rag\_vectorstore/         # Auto-generated Chroma DB (ignored)





---

\## ⚙️ Setup Instructions



\### 1. Create a virtual environment



```Bash

python -m venv venv

.\\venv\\Scripts\\activate   # On Windows PowerShell

source venv/bin/activate     # For macOS/Linux:

```

2\. Install dependencies

```Bash

pip install -r requirements.txt

```

3\. Download the embedding model (one time)

```Python

from sentence\_transformers import SentenceTransformer

SentenceTransformer('BAAI/bge-small-en-v1.5').save('./models/bge-small-en-v1.5')

```

Note: This will download the model to the ./models/bge-small-en-v1.5 directory. See models/README.md for more details.

4\. Populate my\_style/ (Your Custom Code Examples)

Place your custom code files (e.g., .py, .js, .css, etc.) into the my\_style/ directory. These files will be used to train the RAG system on your preferred coding style. The application will automatically synchronize your rag\_vectorstore with changes in this directory.

5\. Start Ollama Server and Download CodeLlama Model

Ensure Ollama is installed and running on your system. Then, download the codellama:7b-instruct model:

```Bash

ollama run codellama:7b-instruct

```

6\. Run the app

```Bash

streamlit run app.py

```
---
📦 Note on Models

The models/ folder and rag\_vectorstore/ are not included in the Git repository to keep the size small. See models/README.md for instructions to download the model locally.

---
🧠 Powered By

1.Streamlit

2.Ollama

3.SentenceTransformers

4.ChromaDB
