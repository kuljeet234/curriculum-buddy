# curriculum-buddy

Streamlit app that turns a course syllabus (PDF / DOCX / TXT) into a curated
set of YouTube playlist links. Uses Google Gemini to extract topics and
generate searchable keywords, then constructs YouTube search URLs.

## Setup

```sh
pip install -r requirements.txt
```

Create a `config.py` (gitignored) at the repo root:

```python
GEMINI_API_KEY = "..."
SERP_API_KEY   = "..."   # optional, for Stack Overflow scraping
```

## Run

```sh
streamlit run app.py
```

Or via the CLI entrypoint:

```sh
python main.py path/to/syllabus.pdf
```

## How it works

1. `modules/extract_text.py` — reads the input file (PyMuPDF for PDF,
   python-docx for DOCX, textract fallback for legacy `.doc`).
2. `modules/gemini_api.py` — two Gemini calls:
   - extract syllabus topics from the raw text
   - generate YouTube-searchable keywords for each topic
3. `modules/youtube_links.py` — builds YouTube search URLs.
4. `modules/scraper.py` — optional Stack Overflow scraper via SERP API.

## Limitations

- Requires Gemini API credit.
- Selenium scraper depends on a Chrome install + driver (managed by
  `webdriver-manager`).
