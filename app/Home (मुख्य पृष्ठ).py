import streamlit as st
from common.pages_header import load_header
from dotenv import load_dotenv

load_dotenv()

load_header("index", "🌾")
st.markdown(st.session_state.config["index_content"])