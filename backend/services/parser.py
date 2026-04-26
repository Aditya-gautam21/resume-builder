import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from llama_cpp import Llama

from backend.services.data_loader import load_data
from backend.utils.prompts import Prompts

load_dotenv()

def json_parser():
    resume_data = load_data()

    # Extraction using local llm model(currently using gemma e4b)
    llm = Llama(
        model_path=os.getenv('LOCAL_MODEL_PATH'),
        n_gpu_layers=8,
        n_ctx=2048,
        verbose=False
        )

    '''
    # Openai llm extraction through api

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv('OPENAI_API_KEY'),
        temperature=0
    )

    '''


    prompt = Prompts.resume_extraction_prompt(resume_data)

    response = llm.create_chat_completion(
        messages=[
            {
                'role':'system',
                'content': 'You extract structured JSON from resumes. Return ONLY valid JSON.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        temperature=0
    )

    return (response['choices'][0]['message']['content'])

if __name__ == '__main__':
    print(json_parser())