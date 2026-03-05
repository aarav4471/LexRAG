from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config.settings import Settings


class ChromaManager:

    def __init__(self):
        self.embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.db = Chroma(
            persist_directory=Settings.CHROMA_PATH,
            embedding_function=self.embedding
        )

    def add_documents(self, docs):
        self.db.add_documents(docs)
        self.db.persist()

    def similarity_search_with_score(self, query_text, k=5):
        # Pass TEXT, not embedding
        return self.db.similarity_search_with_score(query_text, k=k)

    def get_all_documents(self):
        return self.db.get()