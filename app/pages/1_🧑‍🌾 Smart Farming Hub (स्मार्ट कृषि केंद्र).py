import streamlit as st
from common.pages_header import load_header
from utils.vectorstore_handler import similarity_search
from utils.llm_handler import generate_answer

load_header("farmers_portal", "🧑‍🌾")

query = st.text_input(
    label=st.session_state.config["farmer_portal_label"], placeholder=st.session_state.config["farmer_portal_placeholder"]
)

ask_btn = st.button(st.session_state.config["farmer_portal_ask_button"], type="primary", disabled=not query.strip())

if ask_btn:
    with st.spinner(f"🔎 {st.session_state.config['farmer_portal_searching']}"):
        results = similarity_search(query.strip(), top_k=5)

    if not results:
        st.warning(st.session_state.config['farmer_portal_no_doc_error'])

    else:
        chunks = [{"text": r["text"], "source": r["source"]} for r in results]

        with st.spinner(f"⚙️ {st.session_state.config['farmer_portal_generating_answer']}"):
            answer = generate_answer(query, chunks)

        st.markdown(f"### 🌱 {st.session_state.config['farmer_portal_answer_label']}")
        st.success(answer)
        st.space("small")

        with st.expander(f"📚 {st.session_state.config['farmer_portal_supporting_docs'].format(no_of_chunks=len(results))}"):
            for i, result in enumerate(results, 1):
                relevance = max(0.0, 1 - result["score"] / 10)
                pct = round(relevance * 100)

                if pct >= 75:
                    bar_color = "#22c55e"   # green
                    badge_bg = "#dcfce7"
                    badge_text = "#15803d"
                elif pct >= 45:
                    bar_color = "#f59e0b"   # amber
                    badge_bg = "#fef3c7"
                    badge_text = "#92400e"
                else:
                    bar_color = "#ef4444"   # red
                    badge_bg = "#fee2e2"
                    badge_text = "#991b1b"

                st.html(f"""
                    <div style="
                        border: 1px solid #e2e8f0;
                        border-radius: 12px;
                        padding: 18px 22px;
                        margin-bottom: 14px;
                        background: #ffffff;
                        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
                        font-family: 'Segoe UI', sans-serif;
                    ">
                        <!-- Header row -->
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                            <span style="font-weight: 700; font-size: 14px; color: #1e293b;">
                                {st.session_state.config['farmer_portal_chunk']} {i}
                            </span>
                            <span style="
                                font-size: 12px;
                                font-weight: 600;
                                padding: 3px 10px;
                                border-radius: 999px;
                                background: {badge_bg};
                                color: {badge_text};
                            ">{pct}% relevance</span>
                        </div>

                        <!-- Relevance bar -->
                        <div style="background: #f1f5f9; border-radius: 999px; height: 5px; margin-bottom: 12px;">
                            <div style="
                                width: {pct}%;
                                height: 100%;
                                background: {bar_color};
                                border-radius: 999px;
                                transition: width 0.4s ease;
                            "></div>
                        </div>

                        <!-- Source -->
                        <div style="
                            font-size: 12px;
                            color: #64748b;
                            margin-bottom: 10px;
                            display: flex;
                            align-items: center;
                            gap: 5px;
                        ">
                            📄 <span style="font-weight: 500;">{result['source']}</span>
                        </div>

                        <!-- Text content -->
                        <div style="
                            font-size: 14px;
                            color: #334155;
                            line-height: 1.65;
                            border-top: 1px solid #f1f5f9;
                            padding-top: 10px;
                        ">
                            {result['text']}
                        </div>
                    </div>
                """)
