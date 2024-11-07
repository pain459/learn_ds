import requests
import fitz  # PyMuPDF
from transformers import AutoTokenizer

# Function to fetch and clean text from a Wikipedia page
def fetch_wikipedia_page(page_title):
    # Wikipedia API endpoint for page summary
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No content found.")
    else:
        print(f"Error fetching Wikipedia page: {response.status_code}")
        return None

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text("text")
    return text

# Tokenizing the text for LLaMA
def tokenize_text(text, tokenizer_model="bert-base-uncased"):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_model)
    tokens = tokenizer(text, truncation=True, padding='max_length', max_length=512, return_tensors="pt")
    return tokens

# Main execution
def preprocess_document(source_type, source_path_or_title):
    if source_type == "wikipedia":
        text = fetch_wikipedia_page(source_path_or_title)
    elif source_type == "pdf":
        text = extract_text_from_pdf(source_path_or_title)
    else:
        raise ValueError("Invalid source_type. Use 'wikipedia' or 'pdf'.")

    if text:
        tokens = tokenize_text(text)
        print(f"Tokenized {len(tokens['input_ids'][0])} tokens.")
        return tokens

# Example Usage
# To preprocess a Wikipedia page
tokens = preprocess_document("wikipedia", "Visakhapatnam")

# To preprocess a PDF
# tokens = preprocess_document("pdf", "your_document.pdf")
