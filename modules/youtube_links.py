import re
import urllib.parse

def get_youtube_links(topics_text):
    lines = topics_text.strip().split("\n")
    links = []

    for line in lines:
        clean_topic = re.sub(r'^[*\-•\d.\s"]+|["]', '', line).strip()
        if clean_topic:
            encoded = urllib.parse.quote(clean_topic)
            links.append(f"{clean_topic} ➤ https://www.youtube.com/results?search_query={encoded}")

    return links
