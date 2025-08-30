import os
import json
import requests
import streamlit as st
from sentence_transformers import SentenceTransformer
import chromadb

# ------------------- Config -------------------
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL = "codellama:7b-instruct"
SYSTEM_PROMPT = "You are an advanced coding assistant designed to generate clean, valid code. Only respond with code—do not provide explanations or commentary. For each query, return a complete, working code snippet in the exact style specified by the user or stored in the RAG database. Always analyze both the functional requirements in the query and the user’s preferred code style from the database before generating your response. Ensure your output strictly matches the desired conventions, formatting, and idioms. Only include the code, with no additional explanations, comments, or preamble. Give the output in the uploaded file format."
DATA_DIR = "./my_style"
EMBED_MODEL_PATH = "./models/bge-small-en-v1.5"  # ✅ Local embedding model path
# ----------------------------------------------

# 📦 Load or embed RAG code style files
def load_rag_db():
    client = chromadb.PersistentClient(path="./rag_vectorstore")
    collection = client.get_or_create_collection("custom_code_style")

    if collection.count() == 0:
        embedder = SentenceTransformer(EMBED_MODEL_PATH)
        files = []
        texts = []
        for root, _, filenames in os.walk(DATA_DIR):
            for fname in filenames:
                path = os.path.join(root, fname)
                with open(path, "r", encoding="utf-8") as f:
                    texts.append(f.read())
                    files.append(path)

        embeddings = embedder.encode(texts).tolist()
        collection.add(
            documents=texts,
            metadatas=[{"source": f} for f in files],
            ids=[str(i) for i in range(len(files))],
            embeddings=embeddings
        )

    return collection

# 🔍 Retrieve top-k relevant style snippets
def retrieve_similar_code(query, collection, top_k=2):
    embedder = SentenceTransformer(EMBED_MODEL_PATH)
    formatted_query = f"Represent this sentence for retrieval: {query}"
    q_embed = embedder.encode([formatted_query]).tolist()[0]
    results = collection.query(query_embeddings=[q_embed], n_results=top_k)
    return results.get("documents", [[]])[0]  # ✅ Ensures a list of all relevant documents/snippets

# 🧠 Initialize vector database
collection = load_rag_db()

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="🧠 Offline Code Bot (RAG)", page_icon="💻")
st.title("💻 Offline Code Generator (Your Style + RAG)")

uploaded_file = st.file_uploader("📂 Upload a code file (optional)", type=["py", "js", "ts", "java", "cpp", "html", "css"])
user_prompt = st.text_area("💬 Ask a coding question", height=100)

if st.button("💡 Generate Code") and user_prompt.strip():
    code_context = ""

    # Include uploaded code
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        code_context += f"Here is the user's uploaded code:\n\n{file_content}\n\n"

    # 🧠 Add context from retrieved style examples
    with st.spinner("Retrieving your coding style..."):
        retrieved_snippets = retrieve_similar_code(user_prompt, collection)
        code_context += "\n\nHere are similar style examples:\n\n"
        for snippet in retrieved_snippets:
            code_context += snippet + "\n\n"

    # 🔥 Full final prompt
    full_prompt = f"{code_context}User request:\n{user_prompt.strip()}\n\nOnly give code. No explanation."

    code_box = st.empty()
    code_output = ""

    # 🔁 Streamed response from Ollama
    with st.spinner("Generating code..."):
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": MODEL,
                "prompt": full_prompt,
                "system": SYSTEM_PROMPT,
                "stream": True
            },
            stream=True
        )

        for line in response.iter_lines():
            if line:
                line = line.decode("utf-8").replace("data: ", "")
                try:
                    data = json.loads(line)
                    content = data.get("response", "")
                    code_output += content
                    code_box.code(code_output, language="python")  # You can make this dynamic based on file extension
                except json.JSONDecodeError:
                    pass