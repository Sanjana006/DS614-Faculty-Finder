import streamlit as st
import sys
from pathlib import Path
import hashlib
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from recommender.similarity import get_recommendations
from recommender.query_parser import parse_query

st.set_page_config(
    page_title="DAIICT Faculty Finder",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Load CSS ----------
css_path = Path(__file__).parent / "styles.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- Helper Functions ----------
@st.cache_data(ttl=3600)
def get_faculty_photo(name, profile_url):
    """Scrape faculty photo from DAIICT profile page"""
    if not profile_url or profile_url == "-":
        return f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&size=200&background=6366f1&color=fff&bold=true"
        
    try:
        response = requests.get(profile_url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find the faculty photo - adjust selector based on actual page structure
            # Common patterns for faculty photos on academic sites
            img = soup.find('img', class_='faculty-photo') or \
                  soup.find('img', alt=lambda x: x and 'photo' in x.lower()) or \
                  soup.select_one('.profile-image img') or \
                  soup.select_one('img[src*="faculty"]') or \
                  soup.select_one('img[src*="staff"]')
            
            if img and img.get('src'):
                img_url = img['src']
                # Make absolute URL if relative
                if img_url.startswith('/'):
                    img_url = f"https://www.daiict.ac.in{img_url}"
                elif not img_url.startswith('http'):
                    # Handle other relative paths if needed
                    base_url = "/".join(profile_url.split("/")[:3])
                    img_url = f"{base_url}/{img_url.lstrip('/')}"
                return img_url
    except Exception:
        pass
    
    # Fallback to initials-based avatar
    return f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&size=200&background=6366f1&color=fff&bold=true"

def extract_keywords(text, max_keywords=8):
    if not text or text == "-":
        return []
    
    keywords = []
    # Handle cases where text might be a string representation of a list
    if text.startswith('[') and text.endswith(']'):
        try:
            import ast
            items = ast.literal_eval(text)
            if isinstance(items, list):
                keywords = [str(k).strip() for k in items if k]
        except:
            pass
            
    if not keywords:
        for delimiter in [',', ';', '|', '\n']:
            if delimiter in text:
                keywords = [k.strip() for k in text.split(delimiter) if k.strip()]
                break
    
    if not keywords:
        words = text.split()
        keywords = [' '.join(words[i:i+3]) for i in range(0, min(len(words), 15), 3)]
    
    cleaned_keywords = []
    for kw in keywords:
        # Extra cleaning
        kw = kw.replace('[', '').replace(']', '').replace("'", '').replace('"', '').strip()
        if kw and 'not_available' not in kw.lower() and len(kw) > 2:
            cleaned_keywords.append(kw)
            if len(cleaned_keywords) >= max_keywords:
                break
    
    return cleaned_keywords

# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>🎓 DAIICT Faculty Finder</h1>
    <p>Discover faculty members matching your research interests with high precision</p>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ⚙️ Display Settings")
    show_scores = st.toggle("Show Match Scores", True, help="Display similarity scores")
    show_keywords = st.toggle("Show Keywords", True, help="Display research keywords as tags")
    
    st.markdown("---")
    st.markdown("### 💡 Smart Search Tips")
    st.markdown("""
    **Specify number of results:**
    - "top 3 machine learning"
    - "5 best computer vision"
    - "first 10 IoT experts"
    
    **Or just search:**
    - "machine learning"
    - "VLSI design"
    
    *Default: 5 results*
    """)

# ---------- Search Input ----------
col_search_1, col_search_2 = st.columns([4, 1])

with col_search_1:
    query = st.text_input(
        "🔍 Search by research interest or expertise",
        placeholder="e.g., top 3 machine learning, computer vision, IoT...",
        label_visibility="collapsed"
    )

with col_search_2:
    search_clicked = st.button("🔎 Search", use_container_width=True, type="primary")

# ---------- Search Logic ----------
if search_clicked or query:
    
    if not query.strip():
        if search_clicked:
            st.warning("⚠️ Please enter a research interest or keyword")
        st.stop()
    
    clean_query, top_k = parse_query(query)
    
    with st.spinner("🔍 Analyzing faculty profiles..."):
        results = get_recommendations(clean_query, top_k)
    
    if not results:
        st.error("❌ No matching faculty found. Try different keywords.")
        st.stop()
    
    st.success(f"✅ Found {len(results)} matching faculty member{'s' if len(results) > 1 else ''}")
    
    for idx, faculty in enumerate(results, start=1):
        # The faculty-card wrapper is applied via a container to avoid white bars
        with st.container():
            st.markdown('<div class="faculty-card">', unsafe_allow_html=True)
            
            col_avatar, col_info, col_score = st.columns([1.5, 4, 1.5])
            
            with col_avatar:
                name = faculty.get('name', 'Faculty')
                profile_url = faculty.get("profile_url", "")
                photo_url = get_faculty_photo(name, profile_url)
                st.markdown(f"""
                <div class="avatar-container">
                    <img src="{photo_url}" class="avatar-img" alt="{name}">
                </div>
                """, unsafe_allow_html=True)
            
            with col_info:
                st.markdown('<div class="faculty-info">', unsafe_allow_html=True)
                
                rank_badge = ""
                if idx == 1: rank_badge = "🥇"
                elif idx == 2: rank_badge = "🥈"
                elif idx == 3: rank_badge = "🥉"
                
                faculty_name = faculty.get('name', 'Unknown')
                st.markdown(f"""
                <div class="faculty-name">
                    <span class="name-text">{faculty_name}</span>
                    <span class="rank-badge">{rank_badge}</span>
                </div>
                """, unsafe_allow_html=True)
                
                email = faculty.get("mail", "")
                if email:
                    st.markdown(f'''
                    <div class="email-info">
                        <a href="mailto:{email}">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 4px;"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                            {email}
                        </a>
                    </div>
                    ''', unsafe_allow_html=True)
                
                if show_keywords:
                    specialization = faculty.get("specialization", "")
                    research = faculty.get("research", "")
                    combined_text = f"{specialization} {research}"
                    keywords = extract_keywords(combined_text)
                    
                    if keywords:
                        keywords_html = "".join([f'<span class="keyword-tag">{kw}</span>' for kw in keywords])
                        st.markdown(f'<div class="keywords-container">{keywords_html}</div>', unsafe_allow_html=True)
                
                if profile_url and profile_url != "-":
                    st.markdown(f"""
                    <div style="margin-top: 1.5rem;">
                        <a href="{profile_url}" target="_blank" style="font-size: 0.9rem; letter-spacing: 0.02em;">
                            Full Profile Details ↗
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True) # End faculty-info
            
            with col_score:
                if show_scores:
                    score = faculty.get("score", 0)
                    score_percent = int(score * 100)
                    st.markdown(f"""
                    <div class="score-container">
                        <div class="score-label">MATCH SCORE</div>
                        <div class="score-value">{score_percent}%</div>
                        <div class="score-bar">
                            <div class="score-fill" style="width: {score_percent}%"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True) # End faculty-card


# ---------- Footer ----------
if not search_clicked:
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🎯 Enter your research interests above to find matching faculty members</p>
        <p style="font-size: 0.9em;">Powered by Team "The Data Engineers"</p>
    </div>
    """, unsafe_allow_html=True)
