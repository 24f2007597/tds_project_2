from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_quiz_content(url: str) -> str:
    """
    A simple, robust function to get all visible text from a URL.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage') # Critical for Railway/Docker
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        
        # Wait for the BODY tag to exist. This is all we need.
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Now, just get all the visible text from the body.
        page_text = driver.find_element(By.TAG_NAME, 'body').text
        
        # Check if it's empty
        if not page_text.strip():
            print("Error: Page was blank.")
            return "Error: Page was blank or had no text."
            
        return page_text
        
    except Exception as e:
        print(f"Error in get_quiz_content: {e}")
        return f"Error: {e}" # Return the error string
    finally:
        driver.quit()