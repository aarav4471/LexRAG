import os
import re


class Helpers:

    # ===========================
    # Save Uploaded File
    # ===========================
    @staticmethod
    def save_uploaded_file(uploaded_file):
        os.makedirs("temp", exist_ok=True)
        file_path = os.path.join("temp", uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return file_path

    # ===========================
    # Clean Extracted Text
    # ===========================
    @staticmethod
    def clean_text(text):
        if not text:
            return ""
        return re.sub(r"\s+", " ", text).strip()

    # ===========================
    # Extract Case Name (Robust)
    # ===========================
    @staticmethod
    def extract_case_name(text):
        if not text:
            return "Unknown Case"

        # Try common Indian case name formats
        patterns = [
            r"([A-Z][A-Za-z\s]+v\.?\s[A-Z][A-Za-z\s]+?\(\d{4}\))",
            r"([A-Z][A-Za-z\s]+vs\.?\s[A-Z][A-Za-z\s]+?\(\d{4}\))",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()

        # Fallback: find first line containing "vs"
        for line in text.split("\n"):
            if " vs " in line.lower():
                return line.strip()

        return "Unknown Case"

    # ===========================
    # Extract Year
    # ===========================
    @staticmethod
    def extract_year(text):
        if not text:
            return "Unknown"

        match = re.search(r"\((\d{4})\)", text)
        if match:
            return match.group(1)

        return "Unknown"