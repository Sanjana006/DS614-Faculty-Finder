import streamlit as st
import requests

API_URL = "http://localhost:8000/recommend"

st.set_page_config(
    page_title="Faculty Finder",
    layout="wide"
)

st.title("🎓 Faculty Finder")
st.write("Find the best faculty to talk to, collaborate with, or seek guidance from.")

query = st.text_input(
    "Enter your research interest",
    placeholder="e.g. NLP, wireless communication, graph algorithms"
)

top_k = st.slider("Number of recommendations", 1, 10, 5)

if st.button("Find Faculty") and query:
    with st.spinner("Finding best matches..."):
        response = requests.get(
            API_URL,
            params={"query": query, "top_k": top_k}
        )

    if response.status_code == 200:
        data = response.json()
        results = data["recommendations"]

        if not results:
            st.warning("No matching faculty found.")
        else:
            for f in results:
                with st.container():
                    st.subheader(f["name"])
                    st.markdown(f"📧 **Email:** {f['email']}")
                    st.markdown(f"🎯 **Match Score:** `{f['score']}`")
                    st.markdown("**Specialization:**")
                    st.write(f["specialization"])
                    st.divider()
    else:
        st.error("API error. Please try again.")
