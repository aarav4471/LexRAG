import re


class CitationExtractor:

    PATTERNS = [
        r"[A-Z][a-zA-Z]+ vs\.? [A-Z][a-zA-Z]+ \(\d{4}\)",
        r"AIR \d{4} SC \d+"
    ]

    @staticmethod
    def extract(text):
        citations = []
        for pattern in CitationExtractor.PATTERNS:
            citations.extend(re.findall(pattern, text))
        return list(set(citations))