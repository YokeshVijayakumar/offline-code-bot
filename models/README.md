\# 📁 models/ — Local Embedding Model Folder



This folder is used to store the SentenceTransformer embedding model used for retrieval in your offline code bot.



---



\## 🧠 Model Used



\- \*\*Model\*\*: `BAAI/bge-small-en-v1.5`

\- \*\*Purpose\*\*: Embeds your code and user query to retrieve style-consistent code examples via ChromaDB



---



\## ❓ Why This Folder Is Not Committed



This model is large (~120MB), so the folder is \*\*excluded from Git\*\* using `.gitignore` to keep the repo lightweight.



---



\## 📥 How to Download the Model



Run this Python code once in your environment:



```python

from sentence\_transformers import SentenceTransformer

SentenceTransformer('BAAI/bge-small-en-v1.5').save('./models/bge-small-en-v1.5')

Once downloaded, the model will be stored in this folder and used automatically during RAG-based retrieval.



📌 Important

You only need to download this model once.



This folder should remain excluded from Git to avoid uploading large binary data.



