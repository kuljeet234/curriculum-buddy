# modules/scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import time
from pathlib import Path


def search_stackoverflow_link(topic):
    query = f"site:stackoverflow.com {topic}"

    # Generate a random user agent
    ua = UserAgent()
    user_agent = ua.random

    # Setup Brave with headless mode
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={user_agent}")
    options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"  # Update this if needed

    try:
        driver_path = Path("/Users/kuljeetsinghshekhawat/.wdm/drivers/chromedriver/mac64/135.0.7049.84/chromedriver-mac-arm64/chromedriver")
        driver = webdriver.Chrome(service=Service(str(driver_path)), options=options)

        driver.get(f"https://www.google.com/search?q={query}")
        time.sleep(2.5)

        search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g')

        for result in search_results:
            try:
                link_element = result.find_element(By.TAG_NAME, 'a')
                link = link_element.get_attribute('href')

                if "stackoverflow.com/questions" in link:
                    title = result.text.split('\n')[0]
                    print(f"✅ Found StackOverflow: {link}")
                    driver.quit()
                    return {"title": title, "link": link}

            except Exception as e:
                print(f"⚠️ Skipping result due to error: {e}")
                continue

        print("❌ No valid Stack Overflow result found.")
        driver.quit()
        return None

    except Exception as e:
        print(f"🚨 Error during Google scraping: {e}")
        return None
