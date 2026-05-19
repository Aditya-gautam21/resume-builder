import os 
from dotenv import load_dotenv
from llama_cpp import Llama
from langchain_openai import ChatOpenAI

load_dotenv()

def load_local_llm():
    #use local gguf model (currently using google gemma e4b)
    llm = Llama(
    model_path=os.getenv('LOCAL_MODEL_PATH'),
    n_gpu_layers=12,
    n_ctx=4096,
    verbose=False
    )

    return llm

def load_openai_llm():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv('OPENAI_API_KEY'),
        temperature=0
    )

    return llm