import pickle
import sys

from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from utils.constants import DATA_FOLDER, SOURCES_FILE_NAME, OPENAI_EMBEDDING_MODEL, VECTORS_FOLDER_BY_ARTICLE, \
    VECTORS_FOLDER_BY_TEXT_SPLITTING


def by_article_embeddings():
    save_path = f"{DATA_FOLDER}{SOURCES_FILE_NAME}"
    open_file = open(save_path, "rb")
    articles_list = pickle.load(open_file)
    open_file.close()

    document_list = []
    for article in articles_list:
        document_list.append(Document(page_content=article.article_content,
                                      metadata={"source": f"{article.article_number} - {article.article_title}"}))

    Chroma.from_documents(documents=document_list, embedding=OPENAI_EMBEDDING_MODEL,
                          persist_directory=f"{VECTORS_FOLDER_BY_ARTICLE}")


def by_window_chunking():
    save_path = f"{DATA_FOLDER}{SOURCES_FILE_NAME}"
    open_file = open(save_path, "rb")
    articles_list = pickle.load(open_file)
    open_file.close()

    document_list = []
    full_text = ""
    for article in articles_list:
        full_text += article.article_content

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n"],
        chunk_size=20000,
        chunk_overlap=0,
        length_function=len
    )

    texts = text_splitter.create_documents(full_text)
    Chroma.from_documents(documents=texts, embedding=OPENAI_EMBEDDING_MODEL,
                          persist_directory=f"{VECTORS_FOLDER_BY_TEXT_SPLITTING}")


by_article_embeddings()
print("Done")
#by_window_chunking()
#print("Done")
