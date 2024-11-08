from transformers import LlamaTokenizer, AutoModelForCausalLM
import torch

# Define the model and tokenizer paths
model_path = "D:\\src_git\\models\\Llama-3.2-1B"
tokenizer_path = "D:\\src_git\\models\\Llama-3.2-1B\\original"

# Load tokenizer and model directly
try:
    tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    print("Model and tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading model or tokenizer: {e}")
    exit()

# Confirm the type of tokenizer to ensure it loaded correctly
print("Tokenizer type:", type(tokenizer))

# Set the device for model inference
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
print(f"Using device: {device}")

# Define the function to interact with the model
def ask_model(query, max_length=100, temperature=0.7, top_p=0.9):
    if not query:
        print("Query is empty.")
        return None

    try:
        # Tokenize the input query and move it to the device
        inputs = tokenizer(query, return_tensors="pt").to(device)
        # Generate response from the model
        outputs = model.generate(
            inputs["input_ids"],
            max_length=max_length,
            temperature=temperature,
            top_p=top_p
        )
        # Decode the output to get the answer
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer
    except Exception as e:
        print(f"Error during model inference: {e}")
        return f"Error: {e}"

# Test the function with a sample question
question = "What are the common risk factors for heart disease?"
response = ask_model(question)

# Display the response
if response:
    print("Response:", response)
else:
    print("No response generated.")
