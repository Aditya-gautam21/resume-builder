import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

def load_data():
    loader = PyPDFLoader(
        file_path=os.getenv('FILE_PATH')
    )

    data  = loader.load()

    data_txt = " ".join(chunk.page_content for chunk in data)

    '''
    #If the data is to be stored in txt file 

    with open('resume.txt', 'a', encoding='utf-8') as f:
        f.write(data_txt)
    '''

    return data_txt