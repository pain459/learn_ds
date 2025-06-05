import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import requests

model = SentenceTransformer("all-MiniLM-L6-v2")
INDEX_FILE = "vector_store.index"
MAPPING_FILE = "index_mapping.pkl"
OLLAMA_URL = "http://ollama:11434/api/generate"

def search_and_respond(question: str, dataset_name: str = None):
    if not os.path.exists(INDEX_FILE) or not os.path.exists(MAPPING_FILE):
        raise Exception("No training data found.")

    index = faiss.read_index(INDEX_FILE)
    with open(MAPPING_FILE, "rb") as f:
        mapping = pickle.load(f)

    q_vec = model.encode([question])
    D, I = index.search(q_vec, 10)

    context_chunks = []
    for i in I[0]:
        if i >= len(mapping):
            continue
        chunk, tag = mapping[i]
        if dataset_name is None or tag == dataset_name:
            context_chunks.append(chunk)
        if len(context_chunks) >= 3:
            break

    if not context_chunks:
        return f"No data found for dataset: '{dataset_name}'"

    prompt = f"""Use the below context to answer the question.
Context:
{chr(10).join(context_chunks)}

Question:
{question}
"""

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    return response.json().get("response", "[No response]")
