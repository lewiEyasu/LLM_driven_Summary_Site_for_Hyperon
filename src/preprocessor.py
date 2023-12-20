
import json 
import pdfplumber



path = "/home/lewi/Documents/project/llm_summary/LLM_driven_Summary_Site_for_Hyperon/Data/book.pdf"

def clean (texts):
    clean_text = []
    temp  = ''
    for text in texts:
        temp = (text[0].replace("-\n", ""))
        temp = (temp.replace("\n", " "))
        clean_text.append([temp])

    return clean_text   


def chuck_chapters(text, list_pages):
    chapters = []
    
    for index, page in enumerate(list_pages):
        if index < len (list_pages) - 1:
            next_page = list_pages[index + 1]
            chapters.append(" ".join(text[page: next_page][0]))

    return chapters    

def extract_text(path):
    
    result = []
    with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    result.append([page_text])

    return result

