import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

load_dotenv(override=True)

# Cohere
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_EMBEDDING_MODEL = OpenAIEmbeddings()
OPENAI_LLM_MODEL = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Database
DATA_FOLDER = "data"
SOURCES_FILE_NAME = "/sources_20240218.pkl"

VECTORS_FOLDER_BY_ARTICLE_SPLIT = "data/vectors/by_article"
VECTORS_FOLDER_BY_FIXED_SIZE_WINDOW_SPLIT = "data/vectors/by_text_splitting"


