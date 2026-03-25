from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_screenshot(url):
    image_path = "screenshot.png" 
    
    # Set up a hidden browser to capture a full-page screenshot
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--hide-scrollbars")
    options.page_load_strategy = 'normal'
    
    try:
        # Visit the URL and take a screenshot
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(10)
        
        if not url.startswith("http"):
            url = "http://" + url
            
        driver.get(url)
        time.sleep(2)  
        driver.save_screenshot(image_path)
        
        # Extract all visible text from the page
        try:
            page_text = driver.find_element("tag name", "body").text
        except:
            page_text = ""
            
        driver.quit()
        return image_path, page_text
        
    except Exception as e:
        print(f"Error capturing URL: {e}")
        if 'driver' in locals():
            driver.quit() 
        return None, ""