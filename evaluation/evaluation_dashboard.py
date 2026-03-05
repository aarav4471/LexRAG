
import streamlit as st
from evaluation.metrics import Evaluator
from evaluation.llm_judge import LLMJudge


def show_evaluation():

    st.title("📊 RAG Evaluation Dashboard")

    st.subheader("Retrieval Evaluation")

    query = st.text_input("Query")

    relevant_case = st.text_input("Relevant Case")

    retrieved_cases = st.text_input(
        "Retrieved Cases (comma separated)"
    )

    answer = st.text_area("Generated Answer")

    context = st.text_area("Retrieved Context")

    if st.button("Run Evaluation"):

        if not relevant_case or not retrieved_cases:
            st.warning("Please provide relevant and retrieved cases.")
            return

        # Convert inputs to lists
        relevant = [relevant_case.strip()]

        retrieved = [
            r.strip()
            for r in retrieved_cases.split(",")
            if r.strip()
        ]

        k = 5

        precision = Evaluator.precision_at_k(relevant, retrieved, k)

        recall = Evaluator.recall_at_k(relevant, retrieved, k)

        mrr = Evaluator.mrr(relevant, retrieved)

        f1 = Evaluator.f1(precision, recall)

        st.subheader("📈 Retrieval Metrics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Precision@K", round(precision, 3))
        col2.metric("Recall@K", round(recall, 3))
        col3.metric("MRR", round(mrr, 3))
        col4.metric("F1 Score", round(f1, 3))

        # -------------------------
        # LLM Judge Evaluation
        # -------------------------

        if answer:

            st.subheader("🤖 LLM-as-a-Judge Evaluation")

            judge = LLMJudge()

            try:

                scores = judge.evaluate(
                    query,
                    answer,
                    context
                )

                st.json(scores)

            except Exception as e:
                st.error(f"Judge evaluation failed: {e}")

