import os
from typing import List
import numpy as np
import pandas as pd
from .utility import get_completion
from .embed import embed_question
from .Sentence_Window_Retrieval import sentence_window
from sklearn.metrics.pairwise import cosine_similarity



# Constants and Configurations
base_dir = (os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
EMBED_PATH = (os.path.join(base_dir, "Data", "embed.npy"))
DATASET_PATH = (os.path.join(base_dir, "Data", "dataset.csv"))
PROMPT = """Write a a wiki page from the given title. use only the information provided from the context. Try to include as many key details as possible."""
PROMPT_test = """Create a comprehensive modern wiki page with the given  title and  based on the provided context. Ensure the page includes relevant information, background details, and organized sections. Pay attention to accuracy, coherence, and clarity in presenting the information. Aim for a well-structured and informative page that aligns with standard wiki formatting and conventions."""

def get_context(dataset, question: str):
    """
    Get context information for a given question.

    Args:
        dataset (pd.DataFrame): The dataset.
        question (str): The question.

    Returns:
        str: The context information.
    """
    # Load context from a file
    context = np.load(EMBED_PATH, allow_pickle=True)

    temp = np.zeros((1,1536))
    for index, i in enumerate(context):
        if index == 0:
            temp = np.array(i)
        else:
                
            temp = np.concatenate((temp, np.array(i)), axis=0) 

    # Process the question
    question_embedding = embed_question(question)

    # Reshape the question vector to be a 2D array
    question_embedding = question_embedding.reshape(1, -1)

    # Ensure all elements in the context array are numerical
    context = np.asarray(temp, dtype=np.float64)

    # Compute cosine similarity for each row in the context
    similarity_scores = cosine_similarity(temp, question_embedding)


    # Get the indices of the top 4 most similar rows
    most_similar_indices = np.argsort(similarity_scores.ravel())[-3:][::-1]

    temp_result = ""
    for index in most_similar_indices:
        temp_result = temp_result + sentence_window(DATASET_PATH, int(index), 20)   

    return temp


def respond_to_context(question: str, input_prompt:str = PROMPT_test):
    """
    Respond to a given question with relevant context information.

    Args:
        question (str): The question.

    Returns:
        str: The response.
    """
    df = pd.read_csv(DATASET_PATH)
    # relevant_id = retrieve_answer_directory(question) - 1
    #
    # if relevant_id == -1:
    #     return "Error: No relevant folder found to answer the given question." 
    if not input_prompt:
        input_prompt = PROMPT_test

    context =  get_context(dataset=df, question=question)    
    prompt = (
    f"""{input_prompt}\n\n\n
    {question}\n\n\n
    {context}\n\n\n
    SUMMARY:\n"""
)

    messages = [
        {'role': 'system', 'content': """You excel at following instructions, writing blog and providing the correct answers. """},
        {'role': 'user', 'content': f"{prompt}"}]

    response = get_completion(messages=messages, model="gpt-4-0125-preview", temperature=0)

    return response


# title = "From Philosophy to Practice: Understanding the Core Principles of PLN"

# result = respond_to_context(title)
# print("From Philosophy to Practice: Understanding the Core Principles of PLN", result)
