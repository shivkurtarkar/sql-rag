from datasets import load_dataset

# Load the synthetic_text_to_sql dataset from Hugging Face
dataset = load_dataset("gretelai/synthetic_text_to_sql")

# Print dataset information
print(dataset)

# Save the dataset locally (optional)
# You can specify the split if needed, e.g., dataset['train']
dataset.save_to_disk("./synthetic_text_to_sql_local")
