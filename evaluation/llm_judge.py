
import json
import re
from services.groq_client import GroqClient


class LLMJudge:

    def __init__(self):
        self.llm = GroqClient()

    def evaluate(self, query, answer, context):

        prompt = f"""
You are a legal AI evaluator.

Evaluate the following AI-generated legal answer.

Question:
{query}

Context from cases:
{context}

AI Answer:
{answer}

Score from 1-10 for:
1. relevance
2. grounding
3. correctness
4. completeness

Return ONLY JSON in this format:

{{
 "relevance": number,
 "grounding": number,
 "correctness": number,
 "completeness": number
}}
"""

        response = self.llm.chat(
            system_prompt="You are a strict AI evaluation judge.",
            user_prompt=prompt
        )

        # Extract JSON safely
        match = re.search(r"\{.*\}", response, re.DOTALL)

        if match:
            return json.loads(match.group())

        return {"error": "Could not parse JSON"}

