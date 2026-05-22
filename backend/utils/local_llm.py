import os
from dotenv import load_dotenv
from llama_cpp import Llama
from langchain_openai import ChatOpenAI

load_dotenv()

_local_llm = None
_openai_llm = None


def load_local_llm():
    global _local_llm
    if _local_llm is None:
        _local_llm = Llama(
            model_path=os.getenv('LOCAL_MODEL_PATH'),
            n_gpu_layers=12,
            n_ctx=4096,
            verbose=False,
        )
    return _local_llm


def load_openai_llm():
    global _openai_llm
    if _openai_llm is None:
        _openai_llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv('OPENAI_API_KEY'),
            temperature=0,
        )
    return _openai_llm