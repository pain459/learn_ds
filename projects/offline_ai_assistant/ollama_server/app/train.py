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

    # Always load fresh from disk
    if os.path.exists(index_path) and os.path.exists(mapping_path):
        index = faiss.read_index(index_path)
        with open(mapping_path, "rb") as f:
            mapping = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(384)
        mapping = []

    # Remove existing entries with same dataset_name
    filtered_mapping = [(chunk, tag) for chunk, tag in mapping if tag != dataset_name]
    filtered_texts = [chunk for chunk, tag in filtered_mapping]
    new_index = faiss.IndexFlatL2(384)

    if filtered_texts:
        filtered_vectors = model.encode(filtered_texts)
        new_index.add(filtered_vectors)

    # Add new dataset entries
    new_index.add(vectors)
    filtered_mapping.extend([(chunk, dataset_name) for chunk in chunks])

    # Save new index + mapping
    faiss.write_index(new_index, index_path)
    with open(mapping_path, "wb") as f:
        pickle.dump(filtered_mapping, f)

    return f"Replaced dataset '{dataset_name}' with {len(chunks)} new chunks."


def list_datasets_with_counts():
    if not os.path.exists(mapping_path):
        return []

    with open(mapping_path, "rb") as f:
        mapping = pickle.load(f)

    dataset_counts = {}
    for _, tag in mapping:
        dataset_counts[tag] = dataset_counts.get(tag, 0) + 1

    return sorted(dataset_counts.items())

def purge_dataset(dataset_name: str):
    if not os.path.exists(index_path) or not os.path.exists(mapping_path):
        raise Exception("No training data found.")

    with open(mapping_path, "rb") as f:
        mapping = pickle.load(f)

    remaining = [(chunk, tag) for chunk, tag in mapping if tag != dataset_name]
    removed_count = len(mapping) - len(remaining)

    if removed_count == 0:
        raise Exception(f"No dataset named '{dataset_name}' found.")

    new_index = faiss.IndexFlatL2(384)
    if remaining:
        texts = [chunk for chunk, _ in remaining]
        vectors = model.encode(texts)
        new_index.add(vectors)

    faiss.write_index(new_index, index_path)
    with open(mapping_path, "wb") as f:
        pickle.dump(remaining, f)

    return f"✅ Removed {removed_count} entries from dataset '{dataset_name}'"
