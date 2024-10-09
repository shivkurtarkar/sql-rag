from datasets import load_from_disk
import pandas as pd

# Reading a Parquet file and displaying its contents
def read_hf_dataset(file_path):
    # Load the dataset from local disk
    try:
        dataset = load_from_disk(file_path)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        exit(1)
    # Convert the 'train' split of the dataset to a Pandas DataFrame
    df = pd.DataFrame(dataset["train"])
    return df
    