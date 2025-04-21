from config import GEMINI_API_KEY, FILE_PATH
from modules.extract_text import get_text
from modules.gemini_api import extract_syllabus_using_gemini, generate_searchable_topics
from modules.youtube_links import get_youtube_links

def main():
    full_text = get_text(FILE_PATH)

    # Step 1: Extract syllabus
    syllabus = extract_syllabus_using_gemini(full_text, GEMINI_API_KEY)
    print("\n📚 Extracted Syllabus:\n")
    print(syllabus)

    # Step 2: Generate simplified search topics
    topics = generate_searchable_topics(syllabus, GEMINI_API_KEY)
    print("\n🔍 Simplified Search Topics:\n")
    print(topics)

    # Step 3: Generate YouTube links
    links = get_youtube_links(topics)
    print("\n🎥 YouTube Links:\n")
    for link in links:
        print(link)

if __name__ == "__main__":
    main()
