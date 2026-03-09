import os
import time
import streamlit as st
import base64
from pathlib import Path

from common.pages_header import load_header
from utils.s3_handler import S3Handler
from utils.vectorstore_handler import vectorize_and_store

load_header("admin", "🛠️")
s3_handler = S3Handler(os.environ.get("AWS_BUCKET_NAME"))


@st.cache_data(ttl=60)
def get_all_files():
    return s3_handler.list_files()


# --- Session state initialization ---
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "is_uploading" not in st.session_state:
    st.session_state.is_uploading = False

if "upload_success" not in st.session_state:
    st.session_state.upload_success = False

if "session_uploads" not in st.session_state:
    st.session_state.session_uploads = set()

if "chunks_added" not in st.session_state:
    st.session_state.chunks_added = 0

# --- Toast on success then rerun ---
if st.session_state.upload_success:
    st.session_state.upload_success = False
    chunks = st.session_state.chunks_added
    st.toast(st.session_state.config["admin_file_uploaded_success"], icon="✅")
    st.toast(
        st.session_state.config["admin_chunks_success"].format(chunks=chunks), icon="✅"
    )
    time.sleep(2)
    st.rerun()

is_locked = st.session_state.is_uploading

source_column, second_column = st.columns([2, 8])

with source_column:
    source_selected = st.selectbox(
        label=st.session_state.config["admin_source_select_title"],
        options=("PDF", "DOCX"),
        disabled=is_locked,
    )

with second_column:
    uploaded_file = st.file_uploader(
        st.session_state.config["admin_choose_source_text"].format(
            filetype=source_selected.upper()
        ),
        type=source_selected.lower(),
        key=f"uploader_{st.session_state.uploader_key}",
        disabled=is_locked,
    )

    # --- Button + inline spinner side by side ---
    btn_col, spinner_col = st.columns([3, 5])

    with btn_col:
        upload_btn = st.button(
            label=(
                f"⬆️ {st.session_state.config['admin_upload_btn_text']}"
                if not is_locked
                else f"⬆️ {st.session_state.config['admin_uploading_text']}"
            ),
            disabled=is_locked or uploaded_file is None,
            type="primary",
        )

    with spinner_col:
        if is_locked:
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:10px;height:38px;">
                    <svg width="18" height="18" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg"
                        style="animation:spin 0.8s linear infinite;flex-shrink:0;">
                        <circle cx="9" cy="9" r="7" fill="none" stroke="currentColor"
                            stroke-width="2" stroke-dasharray="28" stroke-dashoffset="10"
                            stroke-linecap="round"/>
                    </svg>
                    <span style="font-size:13px;opacity:0.75;">
                        {st.session_state.config["admin_spinner_text"]}
                    </span>
                </div>
                <style>
                    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
                </style>
                """,
                unsafe_allow_html=True,
            )

    # Step 1: lock UI
    if upload_btn and uploaded_file and not is_locked:
        st.session_state.is_uploading = True
        st.rerun()

    # Step 2: upload to S3 + vectorize
    if st.session_state.is_uploading and uploaded_file:
        file_bytes = uploaded_file.read()

        s3_ok = s3_handler.upload_file_bytes(file_bytes, uploaded_file.name)

        if s3_ok:
            chunks_added = vectorize_and_store(file_bytes, uploaded_file.name)
            st.session_state.upload_success = True
            st.session_state.chunks_added = chunks_added
            st.session_state.session_uploads.add(uploaded_file.name)

        st.session_state.is_uploading = False
        st.session_state.uploader_key += 1
        get_all_files.clear()
        st.rerun()

all_uploaded_files = get_all_files()

BASE_DIR = Path(__file__).resolve().parents[1]
PDF_ICON = BASE_DIR / "assets" / "pdf.svg"
DOCX_ICON = BASE_DIR / "assets" / "docx.svg"


@st.cache_data
def load_icon(icon_path: Path) -> str:
    ext = icon_path.suffix.lower()
    mime = "image/png" if ext == ".png" else "image/svg+xml"
    with open(icon_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def render_documents(files, session_uploads: set):
    is_dark = True

    card_bg = "#1e1e2a"
    card_border = "#2a2a3a"
    card_shadow = "rgba(0,0,0,0.4)"
    text_color = "#f0ede6"
    meta_color = "#888"
    badge_bg = "#2a2a3a"
    badge_color = "#ccc"

    cols = st.columns(3)

    for i, file in enumerate(files):
        col = cols[i % 3]

        with col:
            icon_path = PDF_ICON if file["ext"].lower() == "pdf" else DOCX_ICON
            icon_src = load_icon(icon_path)
            display_name = file["filename"]

            is_new = file["filename"] in session_uploads
            new_badge = (
                f"""
                <div style="
                    position: absolute;
                    overflow: visible;
                    top: -10px;
                    right: -10px;
                    background: linear-gradient(135deg, #22c55e, #16a34a);
                    color: white;
                    font-size: 9px;
                    font-weight: 800;
                    letter-spacing: 1.2px;
                    padding: 3px 8px;
                    border-radius: 20px;
                    text-transform: uppercase;
                    box-shadow: 0 2px 6px rgba(34,197,94,0.4);
                    z-index: 10;
                ">{st.session_state.config['admin_new']}</div>
            """
                if is_new
                else ""
            )

            st.html(
                f"""
                <div style="
                    position:relative;
                    overflow:visible;
                    border-radius:14px;
                    padding:18px 20px;
                    min-height:155px;
                    display:flex;
                    flex-direction:column;
                    justify-content:space-between;
                    gap:14px;
                    background:{card_bg};
                    border:1px solid {card_border};
                    box-shadow:0 4px 16px {card_shadow};
                ">
                    {new_badge}

                    <div style="display:flex;gap:12px;align-items:flex-start;">
                        <img src="{icon_src}" style="width:28px;height:32px;flex-shrink:0;" />
                        <span style="
                            font-size:13px; font-weight:600;
                            color:{text_color};
                            line-height:1.45;
                            word-break:break-word;
                            overflow-wrap:break-word;
                            padding-right:36px;
                        ">{display_name}</span>
                    </div>

                    <div style="
                        display:flex; justify-content:space-between;
                        align-items:center; font-size:12px;
                        color:{meta_color};
                    ">
                        <span>{file["size_kb"]} KB</span>
                        <span style="
                            background:{badge_bg};
                            color:{badge_color};
                            padding:3px 10px; border-radius:8px;
                            font-weight:600; font-size:11px; letter-spacing:0.5px;
                        ">{file["ext"]}</span>
                    </div>
                </div>
                """
            )


st.space("small")
st.markdown(f"### 📚 {st.session_state.config["admin_ks_title"]}")
if not all_uploaded_files:
    st.html(
        f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            gap: 12px;
            opacity: 0.5;
        ">
            <div style="font-size: 36px;">🗄️</div>
            <div style="
                font-size: 15px;
                font-weight: 600;
                color: #ffffff;
            ">
                {st.session_state.config["admin_ndocs_message"]}
            </div>
            <div style="
                font-size: 12px;
                color: #888;
                text-align: center;
                max-width: 260px;
                line-height: 1.6;
            ">
                {st.session_state.config["admin_ndocs_subtitle"]}
            </div>
        </div>
    """
    )
else:
    render_documents(all_uploaded_files, st.session_state.session_uploads)