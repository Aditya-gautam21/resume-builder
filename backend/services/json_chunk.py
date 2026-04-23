import os
from dotenv import load_dotenv
from llama_cpp import Llama

from backend.services.parser import json_parser
from backend.utils.prompts import Prompts

load_dotenv()

parsed_json = json_parser()
prompt = Prompts.json_chunking(parsed_json)

llm = Llama(
    model_path=os.getenv('LOCAL_MODEL_PATH'),
    n_ctx=2048,
    n_gpu_layers=14,
    verbose=False
)

response = llm.create_chat_completion(
    messages=[
        {
            'role':'system',
            'content':prompt
        },
        {
            'role':'user',
            'content':parsed_json
        }
    ],
    temperature=0
)

print(response['choices'][0]['message']['content'])