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
    
    # 🚨 FIX 1: High-res 1080p Desktop Window (Prevents squishing/blurriness)
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--hide-scrollbars") # Keeps the screenshot clean
    options.page_load_strategy = 'normal'
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(10)
        
        if not url.startswith("http"):
            url = "http://" + url
            
        driver.get(url)
        time.sleep(2)  
        
        # 🚨 FIX 2: Grabs only the top "viewport" (smart crop) natively
        driver.save_screenshot(image_path)
        
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