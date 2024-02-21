import logging

import streamlit as st
from chat_uis.ui_by_article_chunking import chat_ui_by_article
from chat_uis.ui_by_window_chunking import chat_ui_by_window

logging.basicConfig(level=logging.INFO)

available_uis = {
    "Ui with article chunking": chat_ui_by_article,
    "ui with fixed size window chunking": chat_ui_by_window
}

st.set_page_config(
    page_title="CRR Bot", page_icon="🤖", layout="wide"
)

if "init_main" not in st.session_state:
    st.session_state["init_main"] = True

with st.sidebar:
    chosen_ui = st.selectbox("Choose view", available_uis.keys(), index=0)

available_uis[chosen_ui]()
