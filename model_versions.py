from langchain.chains import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import ParentDocumentRetriever
from langchain.retrievers import EnsembleRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.storage import InMemoryStore
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate

from utils.constants import VECTORS_FOLDER_BY_ARTICLE_SPLIT, OPENAI_EMBEDDING_MODEL, OPENAI_LLM_MODEL, \
    VECTORS_FOLDER_BY_FIXED_SIZE_WINDOW_SPLIT_NO_METADATA, VECTORS_FOLDER_BY_FIXED_SIZE_WINDOW_SPLIT_WITH_METADATA

QA_PROMPT = PromptTemplate(template=
"""You are in charge of answering questions about an European Banking Regulation called CRR. You are now receiving a question and some context. The context is composed by many articles of the CRR. 
Answer in two sentences using the context mentioning the articles you use explicitly. Combine multiple articles to create a more complete answer. 
                            
Question: {question}
Context: \n\n {summaries}""", input_variables=["summaries", "question"])

DOC_PROMPT = PromptTemplate(
    template="Content: {page_content}\nSource {source}",
    input_variables=["page_content", "source"])

qa_chain = load_qa_with_sources_chain(llm=OPENAI_LLM_MODEL, chain_type="stuff",
                                      prompt=QA_PROMPT, 
                                      document_prompt=DOC_PROMPT, verbose=True) 


def model_from_article_split(prompt):
    vectors_db_articles = Chroma(persist_directory=VECTORS_FOLDER_BY_ARTICLE_SPLIT, 
                        embedding_function=OPENAI_EMBEDDING_MODEL)
    
    vectors_db_chunks = Chroma(persist_directory=VECTORS_FOLDER_BY_FIXED_SIZE_WINDOW_SPLIT_WITH_METADATA,
                        embedding_function=OPENAI_EMBEDDING_MODEL)
    
    retriever_chunks = vectors_db_chunks.as_retriever()
    retriever_articles = vectors_db_articles.as_retriever()

    retriever = EnsembleRetriever(retrievers=[retriever_articles, retriever_chunks], weights=[0.5, 0.5])
    chain = RetrievalQAWithSourcesChain(combine_documents_chain=qa_chain, retriever=retriever,
                                     return_source_documents=True, verbose=True)
    
    result = chain.invoke(prompt)
    return result


def model_from_fixed_size_window_split(prompt):
    vectors_db = Chroma(persist_directory=VECTORS_FOLDER_BY_FIXED_SIZE_WINDOW_SPLIT_NO_METADATA,
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
