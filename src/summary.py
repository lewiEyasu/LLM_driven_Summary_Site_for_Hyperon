import os
from typing import List
import numpy as np
import pandas as pd
from scipy import spatial
from utility import get_completion
from embed import embed_question
from sklearn.metrics.pairwise import cosine_similarity



# Constants and Configurations
base_dir = (os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
EMBED_PATH = (os.path.join(base_dir, "Data", "embed.npy"))
DATASET_PATH = (os.path.join(base_dir, "Data", "dataset.csv"))

def distances_from_embeddings(
        query_embedding: List[float],
        embeddings: List[List[float]],
        distance_metric="cosine",
) -> List[List]:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances



def get_context(dataset, question: str):
    """
    Get context information for a given question.

    Args:
        dataset (pd.DataFrame): The dataset.
        question (str): The question.

    Returns:
        str: The context information.
    """
    # result_frame = pd.DataFrame()
    # size = dataset.shape[0]
    # print(size)
    # for context_id in range(size):
    #     # context_id = 7
    #     # path = dataset['path'][context_id]
    #     context = (dataset['text'][context_id])
        

    #     result = pd.DataFrame({'text': [context]})
    #     context_embed = np.load(EMBED_PATH, allow_pickle=True)[context_id]
    #     question_embed = embed_question(question)
    #     result['distances'] = distances_from_embeddings(
    #         question_embed, context_embed, distance_metric='cosine') if question_embed is not None else 100
    #     result_frame = result_frame.append(result, ignore_index=True)
        # break
    # temp = []
    # result_frame.drop_duplicates(['text'], inplace=True)
    # result_frame.sort_values('distances', ascending=True, inplace=True)
    # for text in (result_frame[:7])["text"]:
    #     temp.append(text)

    # return " ".join(temp)



    

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

    # Get the index of the most similar row
    most_similar_index = np.argmax(similarity_scores)

    # Get the similarity score for the most similar row
    most_similar_score = similarity_scores[most_similar_index, 0]
    print(most_similar_score, most_similar_index)
    context = (dataset['text'][most_similar_index-1])
    return context

def respond_to_context(question: str):
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

    context = get_context(dataset=df, question=question)
    print(context)
    # prompt = f"""Context information is below.\n
    # ---------------------\n
    # {context}\n
    # ---------------------\n
    # Given only the context information and not prior knowledge, 
    # answer the query.\n
    # Query: {question}\n
    # Answer: """

    # messages = [
    #     {'role': 'system', 'content': """You excel at following instructions and providing the correct answers."""},
    #     {'role': 'user', 'content': f"{prompt}"}]

    # response = get_completion(messages=messages, model="gpt-4-1106-preview", temperature=0)

    # return response


title = "From Philosophy to Practice: Understanding the Core Principles of PLN"

result = respond_to_context(title)
print("From Philosophy to Practice: Understanding the Core Principles of PLN", result)
