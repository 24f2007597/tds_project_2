from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import os

load_dotenv("secrets.env")
def scrape_website(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds

        wait.until(
            lambda d: d.find_element(By.TAG_NAME, "html")
        )

        full_html = driver.page_source

        return full_html.strip()

    except Exception as e:
        print(f"Error: Timed out waiting for 'body' tag to be populated: {e}")
        driver.quit()
        return None

    finally:
        driver.quit()

if not os.path.exists('sample_quiz.html'):
    print("--- ❌ Failure! 'sample_quiz.html' file not found. ---")
else:
    print("--- Testing get_quiz_content locally ---")
    local_url = 'file://' + os.path.abspath('sample_quiz.html')
    
    quiz_text = scrape_website(local_url)
    
    if quiz_text:
        print("\n--- ✅ Success! Decoded Quiz Text ---")
        print(quiz_text)
    else:
        print("\n--- ❌ Failure! No text decoded ---")