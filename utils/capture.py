from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_screenshot(url):
    image_path = "screenshot.png" 
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,720")
    options.page_load_strategy = 'normal' # Better for getting text
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(10)
        
        if not url.startswith("http"):
            url = "http://" + url
            
        driver.get(url)
        time.sleep(2)  
        
        driver.save_screenshot(image_path)
        
        # 🚨 NEW: Grab the text from the website for the NLP model!
        try:
            page_text = driver.find_element("tag name", "body").text
        except:
            page_text = ""
            
        driver.quit()
        return image_path, page_text # Return both!
        
    except Exception as e:
        print(f"Error capturing URL: {e}")
        if 'driver' in locals():
            driver.quit() 
        return None, ""