import requests

def extract_syllabus_using_gemini(full_text, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    prompt = (
        "Extract the **syllabus only** from this course handout in a clear **point-wise format**. "
        "Do not include course outcomes, course numbers, course details, textbooks, or other sections. "
        "Be precise and avoid skipping any syllabus points.\n\n"
        + full_text
    )

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            content = response.json()
            return content['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"Error parsing response: {e}"
    else:
        return f"API Error: {response.status_code} - {response.text}"

def generate_searchable_topics(syllabus_text, api_key):
    prompt = (
        "The following is a very detailed syllabus:\n\n"
        f"{syllabus_text}\n\n"
        "Please simplify it into 8-12 high-level, YouTube-searchable topics. "
        "Group similar ideas and return each as a short phrase suitable for YouTube search. "
        "Just return the list. Example: ['Number System Basics', 'Digital Logic Gates', 'Combinational Circuits']"
        
    )

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}",
        headers={"Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )

    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Failed to generate topics: {response.status_code}"
