import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_screenshot(url, output_path="screenshots/target_site.png"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1280,720")
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(2)
        driver.save_screenshot(output_path)
        driver.quit()
        return output_path
    except Exception:
        return None