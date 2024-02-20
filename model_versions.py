from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate

from utils.constants import VECTORS_FOLDER_BY_ARTICLE, OPENAI_EMBEDDING_MODEL, OPENAI_LLM_MODEL

PROMPT = PromptTemplate.from_template("""You are an expert in the CRR regulation. 
            This is a complex document used for regulatory purposes by the EU parliament.
            Reply in the most complete way possible, but be precise""")


def model_from_article_split(prompt):
    vectors_db = Chroma(persist_directory=VECTORS_FOLDER_BY_ARTICLE, embedding_function=OPENAI_EMBEDDING_MODEL)
    retriever = vectors_db.as_retriever()
    llm = OPENAI_LLM_MODEL

    chain_type_kwargs = {"prompt": PROMPT}
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return chain.invoke(prompt)
