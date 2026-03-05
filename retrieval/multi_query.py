from services.groq_client import GroqClient


class MultiQueryGenerator:

    def __init__(self):
        self.llm = GroqClient()

    def generate(self, query):

        system = "You are a legal research assistant."
        user = f"""
Generate 4 alternative legal search queries.
Return one per line.

Query:
{query}
"""
        response = self.llm.chat(system, user)

        queries = [
            q.strip("- ").strip()
            for q in response.split("\n")
            if q.strip()
        ]

        return queries[:4]