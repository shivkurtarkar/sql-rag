import pandas as pd
from datasets import load_from_disk

# Load the dataset from local disk
try:
    dataset = load_from_disk("./synthetic_text_to_sql_local")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit(1)

# Convert the 'train' split of the dataset to a Pandas DataFrame
df = pd.DataFrame(dataset["train"])

# Print the DataFrame
print(df)
