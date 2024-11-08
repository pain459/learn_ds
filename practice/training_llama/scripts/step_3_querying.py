from transformers import AutoModelForCausalLM, AutoTokenizer

# Specify the path to the saved model and tokenizer
model_path = "/opt/llama/output/final_model"  # Updated to final model directory
model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True)
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)

# Define the query function
def query_model(prompt, max_length=150):
    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Generate a response from the model
    outputs = model.generate(
        inputs['input_ids'],
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        top_k=50,
        top_p=0.95,
        temperature=0.7
    )
    
    # Decode and return the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Example usage: Ask multiple questions
if __name__ == "__main__":
    print("Type 'exit' to stop querying.")
    while True:
        question = input("Enter your question: ")
        if question.lower() == "exit":
            break
        print("Answer:", query_model(question))
