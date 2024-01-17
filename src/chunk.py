from typing import Any
import pandas as pd
import os
import tiktoken
from glob import glob
from pathlib import Path
import json

ENCODING = tiktoken.encoding_for_model("gpt-3.5-turbo")
CHUNK_SIZE = 200  # The target size of each text chunk in tokens
MIN_CHUNK_SIZE_CHARS = 350  # The minimum size of each text chunk in characters
MIN_CHUNK_LENGTH_TO_EMBED = 5  # Discard chunks shorter than this
MAX_NUM_CHUNKS = 300  # The maximum number of chunks to generate from a text
ENDPAGE_NUM = 282  # the last page number

class Chunk():

    def __init__(self):

        self.base_dir = (os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        self.data_dir_path = os.path.join(self.base_dir, "Data/chuck")
        self.df_total = pd.DataFrame()
        self.dataset_path = (os.path.join(self.base_dir, "Data","dataset.csv"))

            
    def get_json_path(self):
        result = glob(f"{ self.data_dir_path}/*.json")
        return result 
    
    def get_book_title(self, path):
        # Create a Path object
        path_object = Path(path)

        # Get the filename without extension
        filename = path_object.stem

        return filename

    def create_df(self, path):
        book_title = ""
        chapters = []
        load_data = {}
        
        book_title = self.get_book_title(path)
        with open(path, "r") as file:
            load_data = json.load(file)
        chapters = [(f"chapter {index}") for index in range(1,len(load_data['text']) + 1)]
        df = pd.DataFrame({'text': (load_data['text']), 'Title': [book_title] * len(load_data['text']), 'Chapters': chapters})
        return df
        
    def collect_data(self, paths):
        df = pd.DataFrame()
        for path in paths:
            df = pd.concat([df, self.create_df(path)], ignore_index=True)
        return df
            
        

    def get_text_chunks(self, text: str, chunk_token_size: int = CHUNK_SIZE) -> list[str]:
        """Splits a text into chunks of ~CHUNK_SIZE tokens, based on punctuation and newline boundaries.

        Args:
            text (str): Text content to split into chunks.
            chunk_token_size (int, optional): The target size of each chunk in tokens. Defaults to CHUNK_SIZE.

        Returns:
            list: List of text chunks.
        """
        tokens = ENCODING.encode(text)

        chunks = []
        chunk_size = chunk_token_size
        num_chunks = 0

        while tokens:
            chunk = tokens[:chunk_size]

            chunk_text = ENCODING.decode(chunk)

            if not chunk_text or chunk_text.isspace():
                tokens = tokens[len(chunk):]
                continue

            last_punctuation = max(chunk_text.rfind(
                "."), chunk_text.rfind("\n"), chunk_text.rfind("\n\n"))

            if last_punctuation != -1 and last_punctuation > MIN_CHUNK_SIZE_CHARS:
                chunk_text = chunk_text[: last_punctuation + 1]

            chunk_text_to_append = chunk_text.replace("\n", " ").strip()

            if len(chunk_text_to_append) > MIN_CHUNK_LENGTH_TO_EMBED:
                chunks.append(chunk_text_to_append)

            tokens = tokens[len(ENCODING.encode(chunk_text)):]
            num_chunks += 1

        if tokens:
            remaining_text = ENCODING.decode(tokens).replace("\n", " ").strip()
            if len(remaining_text) > MIN_CHUNK_LENGTH_TO_EMBED:
                chunks.append(remaining_text)

        return chunks

    def save_to_csv(self):
        """Saves the processed data to a CSV file."""
        total_test = []

        for key, value in (self.total.items()):
            temp1 = []
            if len(value) > 0:
                for i in value:
                    temp1.append(self.get_text_chunks(i))
                    paths = Path(key)
                    paths = "/".join(paths.parts[-2:])
                total_test.append([paths, temp1])
        df_temp = pd.DataFrame(total_test, columns=['path', 'chuck_text'])
        df_temp.to_csv(os.path.join(
            self.data_dir_path, "dataset.csv"), index=False)


    def chuck_df(self, df):
        temp = []
        chapter = ''
        title = ''
        df_temp= pd.DataFrame()
        for index, row in df.iterrows():
        
            temp = self.get_text_chunks(row.text)
            chapter = row.Chapters
            title = row.Title
            size = len(temp)
            df_temp = pd.DataFrame({'text': temp, 'Title': [title] * size, 'Chapters': [chapter] * size})
            self.df_total = pd.concat([self.df_total,  df_temp], ignore_index=True)

          
        
    def __call__(self ):
            paths = self.get_json_path()
            df = self.collect_data(paths)
            self.chuck_df(df)
            self.df_total.to_csv(self.dataset_path, index=False)
            
        


# test_class = Chunk()
# test_class()
# test_df = test_class.df_total

# print(test_df.info())

# base = (os.path.dirname(os.path.dirname(os.path.realpath(__file__))))        
# print(os.path.join(base, "/Data/dataset.csv"))