
import json 
import pdfplumber



path = "Data/book.pdf"

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
            chapters.append(" ".join([str(item) for item in text[page: next_page]]))

    return chapters    

def extract_text(path):
    
    result = []
    with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    result.append([page_text])

    return result

def save_chapters(text):

    json_file = {}
    json_file["text"] = text
    file_path = "./Data/chuck.json"

    # Write JSON data to a file
    with open(file_path, 'w') as file:
        json.dump(json_file, file, indent=4)

def main():
    result = extract_text(path)
    clean_result = clean(result)
    with open('Data/content.json', 'r') as file:
        # Load JSON data from the file into a Python object
        list_pages = json.load(file)
    
    chapters = chuck_chapters(clean_result, list(list_pages.values()))
    save_chapters(chapters)

    # return chapters


main()
