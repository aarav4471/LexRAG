import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

class Settings:
    try: 
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except Exception:
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = "llama-3.1-8b-instant"
    CHROMA_PATH = "./chroma_db"
 