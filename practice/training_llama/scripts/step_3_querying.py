def query_model(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=150)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Example query
question = "What is machine learning?"
print(query_model(question))
