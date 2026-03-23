from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_screenshot(url):
    image_path = "screenshots/temp_capture.png" 
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,720")
    
    options.page_load_strategy = 'none' 
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.set_page_load_timeout(5)
        
        if not url.startswith("http"):
            url = "http://" + url
            
        driver.get(url)
        
        time.sleep(2)  
        
        driver.save_screenshot(image_path)
        driver.quit()
        
        return image_path
        
    except Exception as e:
        print(f"Error capturing URL: {e}")
        if 'driver' in locals():
            driver.quit() 
        return None