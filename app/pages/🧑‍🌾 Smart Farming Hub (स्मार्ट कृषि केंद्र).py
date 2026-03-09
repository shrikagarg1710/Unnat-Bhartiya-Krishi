import streamlit as st
from common.pages_header import load_header
from utils.vectorstore_handler import similarity_search
from utils.llm_handler import generate_answer

load_header("farmers_portal", "🧑‍🌾")

query = st.text_input(
    label="Ask your farming question", placeholder="What is PM-KISAN?"
)

ask_btn = st.button("Ask", type="primary", disabled=not query.strip())

if ask_btn:
    with st.spinner("🔎 Searching farming knowledge..."):
        results = similarity_search(query.strip(), top_k=5)

    if not results:
        st.warning("No relevant information found in the knowledge base. Please try asking a different question or make sure documents have been uploaded.")

    else:
        chunks = [{"text": r["text"], "source": r["source"]} for r in results]

        with st.spinner("🤖 Generating answer..."):
            answer = generate_answer(query, chunks)

        st.markdown("### 🌱 Answer:")
        st.success(answer)
        st.space("small")

        with st.expander("📚 Supporting Knowledge (Top 5 Chunks)"):
            for i, result in enumerate(results, 1):

                relevance = max(0.0, 1 - result["score"] / 10)
                pct = round(relevance * 100)

                st.markdown(
                    f"""
                    **Chunk {i} — {pct}% relevance**

                    📄 Source: `{result['source']}`

                    {result['text']}

                    ---
                    """
                )
