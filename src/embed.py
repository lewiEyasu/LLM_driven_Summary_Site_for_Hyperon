import os
import openai 
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import time
import numpy as np



# Load your API key from an environment variable or secret management service
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")


base_dir = (os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
data_dir_path = (os.path.join(base_dir, "Data"))

# OpenAI's best embeddings model as of Oct 2023
EMBEDDING_MODEL = "text-embedding-ada-002"


def clean_text(path_text: str = data_dir_path):
    """
    Cleans text from a CSV file.

    Args:
        path_text (str): The path to the directory containing the CSV file.

    Returns:
        list: A list of cleaned text.

    Raises:
        FileNotFoundError: If the specified CSV file is not found.
    """
    try:
        # Load the dataset from the CSV file
        temp_df = pd.read_csv(os.path.join(path_text, 'dataset.csv'))
    except FileNotFoundError:
        raise FileNotFoundError(
            "CSV file 'dataset.csv' not found in the specified directory.")
            

    temp_df.drop(temp_df[(temp_df['text'].str.strip() == '') | (temp_df['text'].str.len() < 10)].index, inplace=True)
    # Extract chuck_text column
    chuck_text = pd.Series(temp_df['text'])

    return chuck_text.values


def embed_question(question: str):
    """
    Embed a question using OpenAI's embedding model.

    Args:
        question (str): The question.

    Returns:
        np.array: Embedding of the question.
    """
    
    try:
        response = openai.embeddings.create(model=EMBEDDING_MODEL,
        input=question)
        return np.array(response.data[0].embedding)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def embed_context(context_list: list):
    """
    Embed a list of contexts using OpenAI's embedding model.

    Args:
        context_list (list): List of contexts.

    Returns:
        np.array: Array of embeddings.
    """
    embeddings = []
    # for index, batch in enumerate(context_list):
    #     flattened = [item for sublist in batch for item in sublist if sublist]

    for i in range(0, len(context_list), 1000):

        batch = context_list[i:i + 1000]
        print(f"start")
        try:
            response = openai.embeddings.create(model=EMBEDDING_MODEL,
            input=list(batch))
            batch_embeddings = [data.embedding for data in response.data]
            embeddings.append(batch_embeddings)
        except Exception as e:
            print(f"An error occurred: {e}")  
        time.sleep(10)  # Due to the rate limit imposed by the OpenAI API.
        
    embed = np.array(embeddings, dtype=object)
    return embed


def save_embeddings(data_dir_path=data_dir_path):
    """
    Save embeddings to a file.

    Args:
        data_dir_path (str): The path to the directory where the embeddings will be saved.

    Returns:
        None
    """
    texts = clean_text(data_dir_path)
    embeddings = embed_context(texts)
    np.save(os.path.join(data_dir_path, "embed.npy"), embeddings)


# save_embeddings()    
