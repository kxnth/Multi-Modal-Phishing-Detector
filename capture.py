from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_screenshot(url):
    # Set up the exact path where you want the image saved
    image_path = "screenshots/temp_capture.png" 
    
    options = Options()
    options.add_argument("--headless=new") # Runs Chrome invisibly
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,720")
    
    # ⚡ SUPERCHARGE FOR SLOW WI-FI: Don't wait for the site to fully load
    options.page_load_strategy = 'none' 
    
    try:
        # Silently install/find the right ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # ⚡ FAST CUTOFF: Only wait 5 seconds max
        driver.set_page_load_timeout(5)
        
        # Ensure the URL has http/https
        if not url.startswith("http"):
            url = "http://" + url
            
        driver.get(url)
        
        # Give it just 2 seconds to draw whatever HTML it managed to grab
        time.sleep(2)  
        
        driver.save_screenshot(image_path)
        driver.quit()
        
        return image_path
        
    except Exception as e:
        print(f"Error capturing URL: {e}")
        # Make sure to quit the driver so it doesn't eat your RAM
        if 'driver' in locals():
            driver.quit() 
        return None