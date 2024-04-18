import pickle
import sys
from pathlib import Path
import os, shutil

from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from utils.constants import DATA_FOLDER, SOURCES_FILE_NAME_OPTIMIZED, SOURCES_FILE_NAME_NON_OPTIMIZED, OPENAI_EMBEDDING_MODEL, VECTORS_FOLDER_BY_FIXED_SIZE_WINDOW_SPLIT_NO_METADATA, VECTORS_FOLDER_BY_FIXED_SIZE_WINDOW_SPLIT_WITH_METADATA, VECTORS_FOLDER_BY_ARTICLE_SPLIT

path = Path(__file__).parent

def delete_content(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    

def by_article_embeddings():
    save_path = path / f"{DATA_FOLDER}{SOURCES_FILE_NAME_OPTIMIZED}"
    open_file = open(save_path, "rb")
    articles_list = pickle.load(open_file)
    open_file.close()

    document_list = []
    for article in articles_list:
        document_list.append(Document(page_content=article.article_content,
                                      metadata={"source": f"{article.article_number} - {article.article_title}"}))
    Chroma.from_documents(documents=document_list, embedding=OPENAI_EMBEDDING_MODEL,
                          persist_directory=f"{VECTORS_FOLDER_BY_ARTICLE_SPLIT}")
    
def by_window_chunking_with_metadata():
    save_path = path / f"{DATA_FOLDER}{SOURCES_FILE_NAME_OPTIMIZED}"
    open_file = open(save_path, "rb")
    articles_list = pickle.load(open_file)
    open_file.close()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks_list = []
    for article in articles_list:
        article_text_split = text_splitter.split_text(article.article_content)
        for article_split in article_text_split:
            chunks_list.append(Document(page_content=article_split,
                                      metadata={"source": f"{article.article_number} - {article.article_title} - Segment"}))

    Chroma.from_documents(documents=chunks_list, embedding=OPENAI_EMBEDDING_MODEL,
                          persist_directory=f"{VECTORS_FOLDER_BY_FIXED_SIZE_WINDOW_SPLIT_WITH_METADATA}")


def by_window_chunking():
    save_path = path / f"{DATA_FOLDER}{SOURCES_FILE_NAME_NON_OPTIMIZED}"
    open_file = open(save_path, "rb")
    articles_list = pickle.load(open_file)
    open_file.close()

    document_list = []
    full_text = ""
    for article in articles_list:
        full_text += article.article_content

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=0,
        length_function=len
    )

    texts = text_splitter.create_documents([full_text])
    Chroma.from_documents(documents=texts, embedding=OPENAI_EMBEDDING_MODEL,
                          persist_directory=f"{VECTORS_FOLDER_BY_FIXED_SIZE_WINDOW_SPLIT_NO_METADATA}")


delete_content(path / f"{VECTORS_FOLDER_BY_ARTICLE_SPLIT}")
delete_content(path / f"{VECTORS_FOLDER_BY_FIXED_SIZE_WINDOW_SPLIT_WITH_METADATA}")
delete_content(path / f"{VECTORS_FOLDER_BY_FIXED_SIZE_WINDOW_SPLIT_NO_METADATA}")

by_article_embeddings()
print("Done")
by_window_chunking_with_metadata()
print("Done")
by_window_chunking()
print("Done")
