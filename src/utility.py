import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)


def get_completion(messages,
                   model,
                   temperature=0,
                   max_tokens=4000):
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

def get_table_content(text):

    messages =  [  
    {"role": "system",
      'content':"""Task: Extract the table of contents enclosed by triple quotes from the given book excerpt.
                   Instructions:

                    1.Locate the section delimited by triple quotes in the book.
                    2.Identify the table of contents within this section.
                    3. Record each chapter/unit and its respective page number.
                    4. Format this information into JSON following this structure:
                          {
                            "Chapter 1": 6,
                            "Chapter 2": 27,
                            "Chapter 3": 44
                          }
                  Ensure the JSON strictly adheres to the specified format, listing chapters/units as keys and their respective page numbers as values."""},    
    {'role':'user', 
    'content':f"""{text}"""},  
    ]
    # print("hallo ", messages)
    return  get_completion(messages=messages, model="gpt-4") 


def handle_response(code: int, message: str, data: str) -> dict:

    return {"code": code,
            "message": message,
            "data": data}