import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

class Settings:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    GROQ_MODEL = "llama-3.1-8b-instant"
    CHROMA_PATH = "./chroma_db"
 