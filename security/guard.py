class SecurityGuard:

    BLOCK_PATTERNS = [
        "ignore previous instructions",
        "override system",
        "forget above",
        "jailbreak",
    ]

    @staticmethod
    def validate_query(query: str):
        lower = query.lower()
        for pattern in SecurityGuard.BLOCK_PATTERNS:
            if pattern in lower:
                raise ValueError("⚠️ Prompt injection detected.")
        return True