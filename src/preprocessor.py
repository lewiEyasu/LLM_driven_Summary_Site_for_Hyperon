import re
import json 
import fitz
from utility import get_table_content
import os
import unicodedata

start = 0

class Proprocessor:
    def __init__(self, path):
    
        self.path = path


    def clean (self, texts):
        clean_text = []
        temp  = ''
    

        for text in texts:

            temp = (str(text).replace("-\n", "").replace("- ", ""))
            temp = temp.replace("\n", " ")
            temp = re.sub(r'[^\x20-\x7E]', '', temp)
            temp =  ''.join(c for c in temp if unicodedata.category(c)[0] != 'C')
            clean_text.append([temp])

        return clean_text   


    def chuck_chapters(self, text, list_pages):
        chapters = []
        
        for index, page in enumerate(list_pages):
          
            if index < len(list_pages)-1:
                start_page = list_pages[index] + start
                next_page = list_pages[index + 1] + start
                print(next_page)
                chapters.append(" ".join([str(item) for item in text[start_page: next_page]]))


        return chapters    

    def extract_text(self):

        doc = fitz.open(self.path)
        result = []
        for page in doc: # iterate the document pages
            result.append(page.get_text()) # get plain text encoded as UTF-8

        return result
    

    def load_book(self):
        table_content = []
        pattern = r"Contents"
        doc = fitz.open(self.path) 
        temp_text = [page.get_text()  for index, page in  enumerate(doc) if index <=25]

        for index, page in  enumerate(temp_text): 
                match = re.search(pattern, page, re.IGNORECASE)
                
                if match:
                    if index+9 <= 24:
                        end = index + 9
                        table_content = [page for page in temp_text[index:end]]
                        
                    else:  
                        table_content = [page for page in temp_text[index:]]
                
                    
                    return ' '.join(map(str, table_content))

    def save_content(self, flag= False):
        file_path = "Data/table_content.json"
        if flag:
            print(get_table_content(self.load_book()))
            json_file = json.loads(get_table_content(self.load_book()))
            
            # Write JSON data to a file
            with open(file_path, 'w') as file:
                json.dump(json_file, file, indent=4)

        return file_path    

    def save_chapters(self, text):

        json_file = {}
        json_file["text"] = text
        file_path = os.path.join("Data/chuck", os.path.basename(self.path).split(".")[0] + ".json")

        # Write JSON data to a file
        with open(file_path, 'w') as file:
            json.dump(json_file, file, indent=4)

    def __call__(self):
        result = self.extract_text()
        clean_result = self.clean(result)
        content_path = self.save_content()
        with open(content_path, 'r') as file:
            # Load JSON data from the file into a Python object
            list_pages = json.load(file)

        list_pages = list(list_pages.values())
        print(str(list_pages), "\n\n\n")
        chapters = self.chuck_chapters(clean_result, list_pages)
        self.save_chapters(chapters)

        return chapters


# main()
path = "/home/lewi/Documents/project/llm_summary/LLM_driven_Summary_Site_for_Hyperon/Data/resources/(Atlantis Thinking Machines 5) Ben Goertzel, Cassio Pennachin, Nil Geisweiller (auth.) - Engineering General Intelligence, Part 1_ A Path to Advanced AGI via Embodied Learning and Cognitive Synergy-At.pdf"
test = Proprocessor(path)
#print(get_table_content(test.load_book()))
print(test()[0])













