from groq import Groq
from config.settings import Settings


class GroqClient:

    def __init__(self):
        if not Settings.GROQ_API_KEY:
            raise ValueError("Missing GROQ_API_KEY")

        self.client = Groq(api_key=Settings.GROQ_API_KEY)

        # Use model from .env or fallback safely
        self.model = Settings.GROQ_MODEL or "llama-3.1-8b-instant"

    def chat(self, system_prompt, user_prompt, temperature=0):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content