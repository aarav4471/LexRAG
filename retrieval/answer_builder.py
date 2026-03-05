from services.groq_client import GroqClient


class AnswerBuilder:

    def __init__(self):
        self.llm = GroqClient()

    def build(self, query, cases):

        context = "\n\n".join(
            [f"Case: {c['case_name']}\nSection: {c['section']}\n{c['content'][:1000]}"
             for c in cases]
        )

        system = """
You are a legal analyst.

IMPORTANT RULES:
- Use ONLY the provided cases.
- Do NOT introduce new case names.
- Do NOT use outside knowledge.
- If insufficient information exists, say:
  "No sufficient precedent found in indexed documents."

Every paragraph must reference one of the provided case names.
"""

        user = f"""
User Query:
{query}

Retrieved Cases:
{context}

Provide:
- Summary
- Legal principles
- Case references
- Confidence (0-100%)
"""

        return self.llm.chat(system, user)