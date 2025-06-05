from sentence_transformers import SentenceTransformer
import os
import faiss
import pickle
from .utils import validate_file_type, read_file_content, chunk_text

model = SentenceTransformer("all-MiniLM-L6-v2")
index_path = "vector_store.index"
mapping_path = "index_mapping.pkl"

# Load existing index/mapping or initialize new
if os.path.exists(index_path):
    index = faiss.read_index(index_path)
    with open(mapping_path, "rb") as f:
        mapping = pickle.load(f)
else:
    index = faiss.IndexFlatL2(384)
    mapping = []

def process_file(file_path):
    ext = validate_file_type(file_path)
    dataset_name = os.path.splitext(os.path.basename(file_path))[0]
    text = read_file_content(file_path, ext)
    chunks = chunk_text(text)

    vectors = model.encode(chunks)
    index.add(vectors)
    mapping.extend([(chunk, dataset_name) for chunk in chunks])

    faiss.write_index(index, index_path)
    with open(mapping_path, "wb") as f:
        pickle.dump(mapping, f)

    return f"Added {len(chunks)} chunks to dataset: {dataset_name}"
