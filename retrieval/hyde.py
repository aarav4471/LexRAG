from services.groq_client import GroqClient
from indexing.chroma_manager import ChromaManager


class HyDERetriever:

    def __init__(self):
        self.llm = GroqClient()
        self.chroma = ChromaManager()

    def generate_hypothetical(self, query):
        system = "You are a senior constitutional judge."
        user = f"Write a detailed ideal legal judgment answering: {query}"
        return self.llm.chat(system, user)

    def embed(self, text):
        return self.chroma.embed_query(text)