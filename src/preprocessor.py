
import json 
import pdfplumber
from utility import get_table_content
start = 1

class Proprocessor:
    def __init__(self, path):
    
        self.path = path


    def clean (self, texts):
        clean_text = []
        temp  = ''
        for text in texts:
            temp = (text[0].replace("-\n", ""))
            temp = (temp.replace("\n", " "))
            clean_text.append([temp])

        return clean_text   


    def chuck_chapters(self, text, list_pages):
        chapters = []
        
        for index, page in enumerate(list_pages):
          
            if index < len (list_pages) - 1:
                next_page = list_pages[index + 1]
                print(next_page)
                chapters.append(" ".join([str(item) for item in text[page: next_page]]))

        return chapters    

    def extract_text(self, path):
        
        result = []
        with pdfplumber.open(self.path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        result.append([page_text])

        return result

    def save_chapters(self, text):

        json_file = {}
        json_file["text"] = text
        file_path = "./Data/new_book.json"

        # Write JSON data to a file
        with open(file_path, 'w') as file:
            json.dump(json_file, file, indent=4)

    def __call__(self):
        result = self.extract_text(self.path)
        clean_result = self.clean(result)
        with open('./Data/new_book.json', 'r') as file:
            # Load JSON data from the file into a Python object
            list_pages = json.load(file)
            print(list_pages.values())
            list_pages =  list(map(lambda x: x + start, list(list_pages.values())))
        
        chapters = self.chuck_chapters(clean_result, (list_pages))
        # self.save_chapters(chapters)

        return chapters


# main()
path = "/home/lewi/Documents/project/llm_summary/LLM_driven_Summary_Site_for_Hyperon/Data/(Atlantis Thinking Machines) Ben Goertzel, Nil Geisweiller, Lucio Coelho, Predrag Janii, Cassio Pennachin - Real-World Reasoning_ Toward Scalable, Uncertain Spatiotemporal,  Contextual and Causal Infe.pdf"

test = Proprocessor(path)

print(test()[0])









