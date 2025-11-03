from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import re
import base64
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

load_dotenv("secrets.env")

def get_quiz_content(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)

        try:
            wait = WebDriverWait(driver, 10) # Wait up to 10 seconds
            
            # This lambda function waits until the innerHTML of #result is not empty
            wait.until(
                lambda d: d.find_element(By.ID, "result").get_attribute("innerHTML").strip() != ""
            )
            
            # Now that it's not empty, get the content
            result_element = driver.find_element(By.ID, "result")
            decoded_text = result_element.get_attribute("innerHTML")
            
            return decoded_text

        except Exception as e:
            print(f"Error: Timed out waiting for '#result' div to be populated: {e}")
            driver.quit()
            return None
        
    except Exception as e:
        return(f"Error retrieving quiz content: {e}")
        
    finally:    
        driver.quit()

'''
if not os.path.exists('sample_quiz.html'):
    print("--- ❌ Failure! 'sample_quiz.html' file not found. ---")
else:
    print("--- Testing get_quiz_content locally ---")
    local_url = 'file://' + os.path.abspath('sample_quiz.html')
    
    quiz_text = get_quiz_content(local_url)
    
    if quiz_text:
        print("\n--- ✅ Success! Decoded Quiz Text ---")
        print(quiz_text)
    else:
        print("\n--- ❌ Failure! No text decoded ---")
'''