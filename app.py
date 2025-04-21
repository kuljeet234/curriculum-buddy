import streamlit as st
import tempfile
from modules.extract_text import get_text
from modules.gemini_api import extract_syllabus_using_gemini, generate_searchable_topics
from modules.youtube_links import get_youtube_links
from config import GEMINI_API_KEY, SERP_API_KEY
from modules.scraper import search_stackoverflow_link





st.set_page_config(page_title="Syllabus to YouTube Assistant", layout="wide")

# === Sidebar ===
with st.sidebar:
    st.title("📘 About")
    st.markdown("This tool extracts topics from course handouts (PDF, DOCX, DOC, TXT) and recommends YouTube playlists.")
    st.markdown("**Help**: Upload a valid file to begin.")
    st.markdown("**Contact**: kuljeet.keys@gmail.com")

# === Main Title ===
st.markdown(
    """
    <h1 style='text-align: center; margin-bottom: 10px;'>📘 Syllabus to YouTube Playlist Assistant</h1>
    <p style='text-align: center;'>Upload a course handout and we’ll generate a YouTube roadmap for you.</p>
    """,
    unsafe_allow_html=True
)


# === Centered Upload Box ===
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Upload PDF, DOCX, DOC, or TXT",
    type=["pdf", "docx", "doc", "txt"],
    label_visibility="collapsed"
)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name.split('.')[-1]) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("⏳ Extracting syllabus and searching YouTube..."):
        full_text = get_text(tmp_path, uploaded_file.name)
        syllabus = extract_syllabus_using_gemini(full_text, GEMINI_API_KEY)
        topics = generate_searchable_topics(syllabus, GEMINI_API_KEY)
        links = get_youtube_links(topics)
        topics_only = [link.split(" ➤ ")[0] for link in links if " ➤ " in link]

    col1, col2 = st.columns(2)

    with col1:
        st.header("📚 Extracted Syllabus")
        st.markdown(
            f"<div style='white-space: pre-wrap; height: 400px; overflow-y: auto; padding: 10px; background-color: #11111122; border-radius: 10px;'>{syllabus}</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.header("🔗 YouTube Links")

        # Scrollable container for YouTube links
        youtube_container = st.container()
        with youtube_container:
            for i, link in enumerate(links, 1):
                if " ➤ " in link:
                    try:
                        topic, url = link.split(" ➤ ")
                        st.markdown(f"**{i}. [{topic}]({url})**", unsafe_allow_html=True)
                    except Exception:
                        st.markdown(f"{link}")  # fallback
                else:
                    st.markdown(link)

        # Extract just topics for later Stack Overflow scraping
        topics_only = [link.split(" ➤ ")[0] for link in links if " ➤ " in link]

        # Button to trigger Stack Overflow scraping
        if st.button("💡 Show Stack Overflow Discussions"):
            with st.spinner("Fetching discussions..."):
                for topic in topics_only:
                    so_result = search_stackoverflow_link(topic)
                    if so_result:
                        st.markdown(
                            f"- **{topic}**: [{so_result['title']}]({so_result['link']})",
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(f"- **{topic}**: No Stack Overflow result found.")





# === Theme Toggle (optional UI hint, handled in settings) ===
st.markdown(
    """
    <style>
        body { transition: background-color 0.2s ease; }
    </style>
    """,
    unsafe_allow_html=True
)

