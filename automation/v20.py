import os
import subprocess
import sys
import time

REQUIRED_MODULES = ["selenium"]


def install_missing_packages():
    for package in REQUIRED_MODULES:
        try:
            __import__(package)
        except ImportError:
            print(f"[!] '{package}' not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def get_user_inputs():
    url = input("Enter the target LimeWire URL: ").strip()

    # Check for chromedriver in current dir
    chromedriver_path = os.path.join(os.getcwd(), "chromedriver")
    if not os.path.exists(chromedriver_path):
        print("[!] ChromeDriver not found in current directory.")
        chromedriver_path = input("Enter full path to your ChromeDriver: ").strip()
        if not os.path.exists(chromedriver_path):
            print("[X] ChromeDriver not found at the given path. Exiting.")
            sys.exit(1)

    return url, chromedriver_path


# Call setup functions
install_missing_packages()

# Now that Selenium is installed, import it
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Gather inputs
url, driver_path = get_user_inputs()

# Selenium options
options = Options()
options.add_argument('--start-maximized')
options.add_argument('--disable-blink-features=AutomationControlled')

# Uncomment if you want to run it headless
# options.add_argument('--headless')

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(url)
    print("[+] Page loaded. Waiting for content...")
    time.sleep(5)

    # Find green Download button
    download_button = driver.find_element(By.XPATH, "//button[contains(@class, 'bg-green') or contains(text(), 'Download')]")
    download_button.click()

    print("[✓] Download button clicked successfully!")
    time.sleep(10)

except Exception as e:
    print(f"[X] Error during execution: {e}")

finally:
    driver.quit()
