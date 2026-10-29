"""JEE Previous Year Papers dashboard (2007-2025).

Run with:   streamlit run app.py
"""
import pandas as pd
import streamlit as st

from utils.pdf_view import read_bytes, viewer_dialog
from utils.scanner import FIRST_YEAR, LAST_YEAR, PAPERS_DIR, folder_stamp, missing_years, scan_papers

st.set_page_config(page_title="JEE Papers Archive", page_icon="📚", layout="wide")


@st.cache_data(show_spinner=False)
def load_papers(_stamp: float) -> list[dict]:
    return scan_papers()


papers = load_papers(folder_stamp())

st.title("📚 JEE Previous Year Papers")
st.caption(f"Question papers {FIRST_YEAR}–{LAST_YEAR} in one place. Filter on the left, then View or Download.")

if not papers:
    st.warning(f"No PDFs found yet. Copy your files into:\n\n`{PAPERS_DIR}`\n\nthen refresh this page.")
    st.stop()

all_years = sorted({p["year"] for p in papers}, reverse=True)
all_exams = sorted({p["exam"] for p in papers})
all_kinds = sorted({p["kind"] for p in papers})

# ------------------------------------------------------------ sidebar filters
with st.sidebar:
    st.header("Filters")
    query = st.text_input("Search", placeholder="year, paper, shift...")
    sel_years = st.multiselect("Year", all_years, format_func=lambda y: str(y) if y else "Other")
    sel_exams = st.multiselect("Exam", all_exams)
    sel_kinds = st.multiselect("Type", all_kinds)
    newest_first = st.radio("Order", ["Newest first", "Oldest first"]) == "Newest first"
    cols_per_row = st.select_slider("Cards per row", options=[1, 2, 3, 4], value=3)
    st.divider()
    if st.button("Rescan papers folder", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

q = query.strip().lower()
items = [
    p for p in papers
    if (not sel_years or p["year"] in sel_years)
    and (not sel_exams or p["exam"] in sel_exams)
    and (not sel_kinds or p["kind"] in sel_kinds)
    and (not q or q in " ".join([p["title"], str(p["year"]), p["exam"], p["paper"], p["shift"], p["kind"]]).lower())
]

# ------------------------------------------------------------ summary
m1, m2, m3 = st.columns(3)
m1.metric("Total papers", len(papers))
m2.metric("Years covered", len({p["year"] for p in papers if p["year"]}))
m3.metric("Showing now", len(items))

gaps = missing_years(papers)
if gaps:
    st.info(f"No files found yet for: {', '.join(map(str, gaps))}")

with st.expander("Papers per year"):
    counts = pd.Series([p["year"] or "Other" for p in papers]).astype(str).value_counts().sort_index()
    st.bar_chart(counts)

# ------------------------------------------------------------ paper cards
if not items:
    st.info("No papers match your filters.")
    st.stop()

by_year: dict[int, list[dict]] = {}
for p in items:
    by_year.setdefault(p["year"], []).append(p)

for year in sorted(by_year, reverse=newest_first):
    group = by_year[year]
    st.subheader(f"{year or 'Other'}  ·  {len(group)} file{'s' if len(group) != 1 else ''}")
    cols = st.columns(cols_per_row)
    for i, p in enumerate(group):
        with cols[i % cols_per_row].container(border=True):
            st.markdown(f"**{p['title']}**")
            tags = [p["exam"], p["paper"], p["shift"], p["kind"] if p["kind"] != "Question Paper" else ""]
            st.caption(" · ".join(t for t in tags if t) + f"  |  {p['size_mb']} MB")
            b1, b2 = st.columns(2)
            if b1.button("View", key=f"view_{p['file']}", type="primary", use_container_width=True):
                viewer_dialog(p)
            b2.download_button("Download", (lambda path=p["path"]: read_bytes(path)), file_name=p["name"],
                               mime="application/pdf", key=f"dl_{p['file']}", use_container_width=True)
