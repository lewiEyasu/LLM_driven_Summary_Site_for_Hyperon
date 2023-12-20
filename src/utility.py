import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)


def get_completion(messages,
                   model,
                   temperature=0,
                   max_tokens=410):
    """Generates a completion for the given messages and model.

    Args:
      messages: A list of messages, where each message is a dictionary with the
        following keys:
          * role: The role of the sender of the message, e.g. "user" or "system".
          * content: The text of the message.
      model: The model to use to generate the completion.
      temperature: The temperature of the model. Higher temperatures result in
        more creative and unpredictable completions.
      max_tokens: The maximum number of tokens to generate.

    Returns:
      A string containing the generated completion.
    """
    response = None
    while response is None:
        try:
            response = client.chat.completions.create(model=model,
            messages=messages,
            temperature=temperature,  # this is the degree of randomness of the model's output
            max_tokens=max_tokens)
        except Exception as e:
            print(e)
            return None
    return response.choices[0].message.content


