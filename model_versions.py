from langchain.chains import RetrievalQA
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate

from utils.constants import VECTORS_FOLDER_BY_ARTICLE_SPLIT, OPENAI_EMBEDDING_MODEL, OPENAI_LLM_MODEL, \
    VECTORS_FOLDER_BY_FIXED_SIZE_WINDOW_SPLIT


def model_from_article_split(prompt):
    vectors_db = Chroma(persist_directory=VECTORS_FOLDER_BY_ARTICLE_SPLIT, embedding_function=OPENAI_EMBEDDING_MODEL)
    retriever = vectors_db.as_retriever()
    llm = OPENAI_LLM_MODEL

    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return chain.invoke(prompt)


def model_from_fixed_size_window_split(prompt):
    vectors_db = Chroma(persist_directory=VECTORS_FOLDER_BY_FIXED_SIZE_WINDOW_SPLIT,
                        embedding_function=OPENAI_EMBEDDING_MODEL)
    retriever = vectors_db.as_retriever()
    llm = OPENAI_LLM_MODEL

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return chain.invoke(prompt)
