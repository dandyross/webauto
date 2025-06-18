from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Path to your ChromeDriver
CHROMEDRIVER_PATH = '/path/to/chromedriver'

# Target URL (from screenshot)
TARGET_URL = 'https://limewire.com/d/uy15P#yLMwWeBxjk'

# Chrome options
options = Options()
options.add_argument('--start-maximized')
options.add_argument('--disable-blink-features=AutomationControlled')
# Comment the next line if you want to see the browser window
# options.add_argument('--headless')

# Set up WebDriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(TARGET_URL)
    time.sleep(5)  # Wait for the page to fully load

    # Click the green Download button (based on class and text)
    download_button = driver.find_element(By.XPATH, "//button[contains(@class, 'bg-green') or contains(text(), 'Download')]")
    download_button.click()

    print("✅ Download button clicked.")

    # Wait for any download prompt or background processing
    time.sleep(10)

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    driver.quit()
