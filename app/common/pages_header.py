import streamlit as st
from streamlit_local_storage import LocalStorage
from configs.en import en_config
from configs.hi import hi_config

def load_header(page, icon):
    DEFAULT_LANG = "English"
    local_storage = LocalStorage()

    def get_config(language: str):
        """Return configuration based on language."""
        if language == "हिन्दी":
            return hi_config
        return en_config

    def init_session():
        """Initialize language and configuration."""
        language = local_storage.getItem("language")

        if language is None:
            language = DEFAULT_LANG
            local_storage.setItem("language", language)

        if "config" not in st.session_state:
            st.session_state.config = get_config(language)

    def update_language():
        """Update language selection."""
        selected_lang = st.session_state.user_language_preference
        local_storage.setItem("language", selected_lang)

        st.session_state.config = get_config(selected_lang)

    # Initialize session state and configuration
    init_session()

    st.set_page_config(page_title=st.session_state.config[f"{page}_title"], page_icon=icon)

    # Index Layout
    title_column, language_column = st.columns([8, 2])

    with language_column:
        selected_language = local_storage.getItem("language") or DEFAULT_LANG

        st.selectbox(
            label="",
            options=("English", "हिन्दी"),
            index=(0 if selected_language == "English" else 1),
            key="user_language_preference",
            on_change=update_language
        )

    with title_column:
        st.title(f"{icon} {st.session_state.config[f'{page}_title']}")