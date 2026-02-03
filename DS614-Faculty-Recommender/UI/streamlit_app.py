import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from recommender.similarity import get_recommendations   # adjust if needed

st.set_page_config(
    page_title="Faculty Recommender",
    page_icon="🎓",
    layout="wide"
)

css_path = Path(__file__).parent / "styles.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.sidebar.title("🔧 Filters")
top_k = st.sidebar.slider("Top Results", 1, 20, 5)

st.title("🎓 Faculty Recommender")
st.caption("Discover the most relevant faculty based on your research interests")

query = st.text_input(
    "Enter your research interest",
    placeholder="machine learning, NLP, databases..."
)

if st.button("Find Faculty 🔍"):

    if not query.strip():
        st.warning("Please enter a research query")
        st.stop()

    with st.spinner("Analyzing faculty profiles..."):
        results = get_recommendations(query, top_k)

    if not results:
        st.error("No matches found")
        st.stop()

    st.success(f"Found {len(results)} matching faculty")

    for r in results:

        with st.container():
            c1, c2 = st.columns([4, 1])

            with c1:
                st.subheader(r.get("name", "Unknown"))
                st.write("**Specialization:**", r.get("specialization", "-"))
                st.write("**Research:**", r.get("research", "-"))
                st.write("**Email:**", r.get("mail", "-"))

            with c2:
                score = r.get("score", 0)
                st.metric("Match", f"{score:.3f}")

        st.divider()
