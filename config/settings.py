import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

class Settings:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")
    CHROMA_PATH = "./chroma_db"
 