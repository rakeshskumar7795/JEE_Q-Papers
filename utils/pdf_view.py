"""PDF reading and display helpers."""
import base64
from pathlib import Path

import streamlit as st


@st.cache_data(show_spinner=False)
def read_bytes(path: str) -> bytes:
    return Path(path).read_bytes()


def show_pdf(data: bytes, height: int = 720) -> None:
    """Native Streamlit PDF viewer, with an embedded-iframe fallback."""
    try:
        st.pdf(data, height=height)
    except Exception:
        b64 = base64.b64encode(data).decode()
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="{height}"></iframe>',
            unsafe_allow_html=True,
        )


@st.dialog("Paper viewer", width="large")
def viewer_dialog(paper: dict) -> None:
    st.subheader(paper["title"])
    tags = [paper["exam"], str(paper["year"] or ""), paper["paper"], paper["shift"], paper["kind"]]
    st.caption(" · ".join(t for t in tags if t))
    data = read_bytes(paper["path"])
    st.download_button("Download PDF", data, file_name=paper["name"], mime="application/pdf", key="dialog_dl")
    show_pdf(data)
