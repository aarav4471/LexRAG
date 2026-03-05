
# import streamlit as st
# import shutil
# import os

# from indexing.chroma_manager import ChromaManager
# from retrieval.multi_query import MultiQueryGenerator
# from retrieval.hyde import HyDERetriever
# from retrieval.answer_builder import AnswerBuilder
# from ingestion.pdf_parser import PDFParser
# from ingestion.image_processor import ImageProcessor
# from indexing.parent_child_indexer import ParentChildIndexer
# from security.guard import SecurityGuard
# from utils.helpers import Helpers
# from config.settings import Settings
# from evaluation.evaluation_dashboard import show_evaluation

# st.set_page_config(layout="wide")
# st.title("🏛 Multimodal Court Case Precedent Finder")

# # Ensure DB folder exists
# os.makedirs(Settings.CHROMA_PATH, exist_ok=True)

# # ===========================
# # Initialize Components
# # ===========================

# if "chroma" not in st.session_state:
#     st.session_state.chroma = ChromaManager()

# chroma = st.session_state.chroma

# multi_query = MultiQueryGenerator()
# hyde = HyDERetriever()
# answer_builder = AnswerBuilder()

# # ===========================
# # SIDEBAR - FILE UPLOAD
# # ===========================

# st.sidebar.header("📂 Upload Legal Documents")

# uploaded_files = st.sidebar.file_uploader(
#     "Upload PDFs or Images",
#     type=["pdf", "png", "jpg", "jpeg"],
#     accept_multiple_files=True
# )

# indexed_count = 0

# if uploaded_files:

#     for uploaded_file in uploaded_files:

#         file_path = Helpers.save_uploaded_file(uploaded_file)

#         try:
#             if uploaded_file.type == "application/pdf":
#                 text = PDFParser.extract_text(file_path)
#             else:
#                if "image_processor" not in st.session_state:
#                    st.session_state.image_processor = ImageProcessor()

#                image_processor = st.session_state.image_processor
#                result = image_processor.process(file_path)
#                text = result["text"]

#             text = Helpers.clean_text(text)

#             case_name = Helpers.extract_case_name(text)
#             year = Helpers.extract_year(text)

#             documents = ParentChildIndexer.split_into_sections(
#                 text, case_name, year
#             )

#             chroma.add_documents(documents)

#             indexed_count += 1
#             st.sidebar.success(f"Indexed: {case_name}")

#         except Exception as e:
#             st.sidebar.error(f"Error processing {uploaded_file.name}: {e}")

#     st.sidebar.info(f"Total Files Indexed: {indexed_count}")

# # ===========================
# # SIDEBAR - INDEXED CASES VIEW
# # ===========================

# st.sidebar.header("📚 Indexed Cases")

# try:
#     all_docs = chroma.get_all_documents()

#     if all_docs and "metadatas" in all_docs and all_docs["metadatas"]:
#         case_names = list(set(
#             meta["case_name"]
#             for meta in all_docs["metadatas"]
#             if "case_name" in meta
#         ))

#         for case in case_names:
#             st.sidebar.write("•", case)
#     else:
#         st.sidebar.write("No cases indexed yet.")

# except:
#     st.sidebar.write("No cases indexed yet.")

# # ===========================
# # MAIN TABS
# # ===========================

# tab1, tab2 = st.tabs(["🔎 Search", "📊 Evaluation"])

# # ===========================
# # TAB 1 - SEARCH
# # ===========================

# with tab1:

#     st.subheader("🔎 Legal Query")

#     query = st.text_input("Enter your legal issue")

#     if st.button("Search"):

#         try:
#             SecurityGuard.validate_query(query)

#             queries = multi_query.generate(query)
#             hypothetical = hyde.generate_hypothetical(query)

#             all_docs = []

#             # Multi-query retrieval
#             for q in queries:
#                 docs = chroma.similarity_search_with_score(q, k=5)
#                 all_docs.extend(docs)

#             # HyDE retrieval
#             hyde_docs = chroma.similarity_search_with_score(hypothetical, k=5)
#             all_docs.extend(hyde_docs)

#             # Deduplicate
#             doc_dict = {}

#             for doc, score in all_docs:
#                 source = doc.metadata["source"]

#                 if source not in doc_dict or score < doc_dict[source][1]:
#                     doc_dict[source] = (doc, score)

#             ranked_docs = sorted(doc_dict.values(), key=lambda x: x[1])

#             # ===============================
#             # NEW: Filter + Top Case Logic
#             # ===============================

#             filtered_docs = []

#             for doc, score in ranked_docs:
#                 similarity = max(0.0, min(1.0, 1 - score))

#                 if similarity >= 0.2:
#                     filtered_docs.append((doc, similarity))

#             if not filtered_docs:
#                 st.warning("No relevant cases found.")

#             else:

#                 st.subheader("📚 Top Similar Cases")

#                 structured_cases = []

#                 # Select the top case
#                 top_case = filtered_docs[0][0].metadata["case_name"]

#                 top_case_chunks = []

#                 for doc, similarity in filtered_docs:

#                     if doc.metadata["case_name"] == top_case:
#                         top_case_chunks.append((doc, similarity))

#                 # Limit to top 3 chunks
#                 top_case_chunks = top_case_chunks[:3]

#                 for doc, similarity in top_case_chunks:

#                     with st.expander(
#                         f"{doc.metadata['case_name']} | Similarity: {round(similarity,3)}"
#                     ):
#                         st.progress(similarity)
#                         st.write(doc.page_content[:1000])

#                     structured_cases.append({
#                         "case_name": doc.metadata["case_name"],
#                         "section": doc.metadata["section"],
#                         "content": doc.page_content
#                     })

#                 st.subheader("🧠 AI Legal Analysis")

#                 answer = answer_builder.build(query, structured_cases)
#                 st.write(answer)

#         except Exception as e:
#             st.error(str(e))

# # ===========================
# # TAB 2 - EVALUATION
# # ===========================

# with tab2:
#     show_evaluation()







import streamlit as st
import os

from indexing.chroma_manager import ChromaManager
from retrieval.multi_query import MultiQueryGenerator
from retrieval.hyde import HyDERetriever
from retrieval.answer_builder import AnswerBuilder
from ingestion.pdf_parser import PDFParser
from ingestion.image_processor import ImageProcessor
from indexing.parent_child_indexer import ParentChildIndexer
from security.guard import SecurityGuard
from utils.helpers import Helpers
from config.settings import Settings
from evaluation.evaluation_dashboard import show_evaluation

import time

def stream_response(text):
    """Stream text while preserving formatting"""
    lines = text.split("\n")
    for line in lines:
        words = line.split(" ")
        for word in words:
            yield word + " "
            time.sleep(0.02)
        yield "\n\n"


st.set_page_config(layout="wide")

st.title("🏛 LexRAG - Advanced Legal Retrieval-Augmented Generation Engine")

# Ensure DB folder exists
os.makedirs(Settings.CHROMA_PATH, exist_ok=True)


# ------------------------------
# Initialize components
# ------------------------------

if "chroma" not in st.session_state:
    st.session_state.chroma = ChromaManager()

chroma = st.session_state.chroma

multi_query = MultiQueryGenerator()
hyde = HyDERetriever()
answer_builder = AnswerBuilder()

if "image_processor" not in st.session_state:
    st.session_state.image_processor = ImageProcessor()

image_processor = st.session_state.image_processor


# ------------------------------
# Sidebar
# ------------------------------

st.sidebar.header("📂 Upload Legal Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs or Images",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:

    with st.spinner("Indexing documents..."):

        for uploaded_file in uploaded_files:

            file_path = Helpers.save_uploaded_file(uploaded_file)

            try:
                if uploaded_file.type == "application/pdf":
                    text = PDFParser.extract_text(file_path)

                else:
                    result = image_processor.process(file_path)
                    text = result["text"]

                text = Helpers.clean_text(text)

                case_name = Helpers.extract_case_name(text)
                year = Helpers.extract_year(text)

                docs = ParentChildIndexer.split_into_sections(
                    text,
                    case_name,
                    year
                )

                chroma.add_documents(docs)

                st.sidebar.success(f"Indexed: {case_name}")

            except Exception as e:
                st.sidebar.error(e)


# ------------------------------
# Sidebar case list
# ------------------------------

st.sidebar.header("📚 Indexed Cases")

try:

    all_docs = chroma.get_all_documents()

    case_names = list(set(
        meta["case_name"]
        for meta in all_docs["metadatas"]
        if "case_name" in meta
    ))

    for case in case_names:
        st.sidebar.write("•", case)

except:
    st.sidebar.write("No cases indexed yet")


# ------------------------------
# Tabs
# ------------------------------

tab1, tab2 = st.tabs(["💬 Chat", "📊 Evaluation"])


# ==============================
# CHAT TAB
# ==============================

with tab1:

    # store chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    # chat input
    prompt = st.chat_input("Ask a legal question...")

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.write(prompt)

        try:

            SecurityGuard.validate_query(prompt)

            queries = multi_query.generate(prompt)
            hypothetical = hyde.generate_hypothetical(prompt)

            all_docs = []

            for q in queries:
                docs = chroma.similarity_search_with_score(q, k=5)
                all_docs.extend(docs)

            hyde_docs = chroma.similarity_search_with_score(
                hypothetical,
                k=5
            )

            all_docs.extend(hyde_docs)

            doc_dict = {}

            for doc, score in all_docs:

                source = doc.metadata["source"]

                if source not in doc_dict or score < doc_dict[source][1]:
                    doc_dict[source] = (doc, score)

            ranked_docs = sorted(
                doc_dict.values(),
                key=lambda x: x[1]
            )

            filtered_docs = []

            for doc, score in ranked_docs:

                similarity = max(0.0, min(1.0, 1 - score))

                if similarity >= 0.2:
                    filtered_docs.append((doc, similarity))

            structured_cases = []

            if filtered_docs:

                top_case = filtered_docs[0][0].metadata["case_name"]

                case_chunks = []

                for doc, similarity in filtered_docs:

                    if doc.metadata["case_name"] == top_case:
                        case_chunks.append((doc, similarity))

                case_chunks = case_chunks[:3]

                for doc, similarity in case_chunks:

                    structured_cases.append({
                        "case_name": doc.metadata["case_name"],
                        "section": doc.metadata["section"],
                        "content": doc.page_content
                    })

            answer = answer_builder.build(prompt, structured_cases)

            with st.chat_message("assistant"):
                st.write_stream(stream_response(answer))
                if structured_cases:
                    st.markdown("### 📚 Retrieved Case Chunks")
                    for case in structured_cases:
                        with st.expander(
                            f"{case['case_name']} | {case['section']}"
                        ):
                            st.write(case["content"][:800])

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(str(e))


# ==============================
# EVALUATION TAB
# ==============================

with tab2:
    show_evaluation()

