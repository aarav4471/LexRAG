import re
from langchain_core.documents import Document


class ParentChildIndexer:

    SECTION_PATTERNS = {
        "facts": r"(Facts.*?)(?=Legal Issue|Arguments|Reasoning|Judgment|$)",
        "legal_issue": r"(Legal Issue.*?)(?=Arguments|Reasoning|Judgment|$)",
        "arguments": r"(Arguments.*?)(?=Reasoning|Judgment|$)",
        "reasoning": r"(Reasoning.*?)(?=Judgment|$)",
        "judgment": r"(Judgment.*?$)"
    }

    @staticmethod
    def split_into_sections(text, case_name, year):

        documents = []

        for section, pattern in ParentChildIndexer.SECTION_PATTERNS.items():
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

            for match in matches:
                documents.append(
                    Document(
                        page_content=match.strip(),
                        metadata={
                            "case_name": case_name,
                            "section": section,
                            "year": year,
                            "source": case_name + "_" + section
                        }
                    )
                )

        return documents