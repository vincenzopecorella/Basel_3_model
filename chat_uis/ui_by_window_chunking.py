import streamlit as st

from chat_uis.chat_utils import st_chat_containers
from model_versions import model_from_article_split, model_from_fixed_size_window_split


def chat_ui_by_window() -> None:
    """Not optimized model"""

    if "init_push_window" not in st.session_state:
        st.session_state["init_push_window"] = True
        st.session_state["messages_push_window"] = []
        st.session_state["cited_docs_window"] = []

    st.title("Not optimized model Chat")

    container1, container2, user_query = st_chat_containers("Chat", "Citations")

    with container1:
        for message in st.session_state["messages_push_window"]:
            with st.chat_message(message["role"]):
                st.markdown(message["message"])

        if user_query:
            st.chat_message("user").markdown(user_query)

            with st.spinner("Thinking..."):
                answer_module = model_from_fixed_size_window_split(user_query)
                ai_answer = answer_module['result']
                st.session_state["cited_docs_window"] = answer_module['source_documents']
                print(answer_module['source_documents'])
            st.chat_message("assistant").markdown(ai_answer)

            st.session_state["messages_push_window"] += [
                {"role": "human", "message": user_query},
                {"role": "ai", "message": ai_answer},
            ]

    with container2:
        for index, doc in enumerate(st.session_state["cited_docs_window"]):
            with st.expander(f"Piece of text n. {index}"):
                st.markdown(doc.page_content)
