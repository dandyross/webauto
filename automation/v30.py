# limewire_downloader.py
import os
import subprocess
import sys
import time
import platform
import urllib.request
import zipfile
import json

REQUIRED_MODULES = ["selenium"]

def install_missing_packages():
    for package in REQUIRED_MODULES:
        try:
            __import__(package)
        except ImportError:
            print(f"[!] '{package}' not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_missing_packages()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def download_driver(browser):
    system = platform.system()
    if browser == "chrome":
        base_url = "https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111"
        suffix = {
            "Windows": "win64/chromedriver-win64.zip",
            "Linux": "linux64/chromedriver-linux64.zip",
            "Darwin": "mac-arm64/chromedriver-mac-arm64.zip"
        }.get(system)
        exe_name = "chromedriver.exe" if system == "Windows" else "chromedriver"
    elif browser == "firefox":
        base_url = "https://github.com/mozilla/geckodriver/releases/download/v0.33.0"
        suffix = {
            "Windows": "geckodriver-v0.33.0-win64.zip",
            "Linux": "geckodriver-v0.33.0-linux64.tar.gz",
            "Darwin": "geckodriver-v0.33.0-macos-aarch64.tar.gz"
        }.get(system)
        exe_name = "geckodriver.exe" if system == "Windows" else "geckodriver"
    elif browser == "edge":
        base_url = "https://msedgedriver.azureedge.net/122.0.2365.92"
        suffix = {
            "Windows": "edgedriver_win64.zip",
            "Linux": "edgedriver_linux64.zip",
            "Darwin": "edgedriver_mac64.zip"
        }.get(system)
        exe_name = "msedgedriver.exe" if system == "Windows" else "msedgedriver"
    else:
        print("[X] Unsupported browser.")
        sys.exit(1)

    if not suffix:
        print("[X] Unsupported OS. Please install the WebDriver manually.")
        sys.exit(1)

    zip_url = f"{base_url}/{suffix}"
    zip_name = "driver.zip"

    print(f"[~] Downloading {browser} driver...")
    urllib.request.urlretrieve(zip_url, zip_name)

    print("[~] Extracting driver...")
    with zipfile.ZipFile(zip_name, 'r') as zip_ref:
        zip_ref.extractall()

    for root, dirs, files in os.walk("."):
        if exe_name in files:
            full_path = os.path.join(root, exe_name)
            final_path = os.path.join(os.getcwd(), exe_name)
            os.rename(full_path, final_path)
            os.remove(zip_name)
            print(f"[✓] {browser.capitalize()}Driver installed.")
            return final_path

    print("[X] Driver extraction failed.")
    sys.exit(1)

def get_user_inputs():
    url = input("Enter the LimeWire URL: ").strip()

    browser = input("Choose browser (chrome/firefox/edge): ").strip().lower()
    driver_name = {
        "chrome": "chromedriver",
        "firefox": "geckodriver",
        "edge": "msedgedriver"
    }.get(browser)

    if not driver_name:
        print("[X] Invalid browser choice.")
        sys.exit(1)

    driver_path = os.path.join(os.getcwd(), driver_name)
    if not os.path.exists(driver_path):
        if input(f"[!] {driver_name} not found. Download it? (y/n): ").strip().lower() == 'y':
            driver_path = download_driver(browser)
        else:
            driver_path = input("Enter path to your WebDriver: ").strip()
            if not os.path.exists(driver_path):
                print("[X] Path not found.")
                sys.exit(1)

    user_agent = None
    if input("Set custom user-agent? (y/n): ").strip().lower() == 'y':
        user_agent = input("Enter User-Agent: ").strip()

    cookies = []
    if input("Load cookies? (y/n): ").strip().lower() == 'y':
        try:
            cookies = json.loads(input("Paste JSON cookie list: "))
        except Exception as e:
            print(f"[!] Invalid JSON: {e}")

    return url, browser, driver_path, user_agent, cookies

def launch_driver(browser, driver_path, user_agent):
    if browser == "chrome":
        options = ChromeOptions()
        if user_agent:
            options.add_argument(f"user-agent={user_agent}")
        return webdriver.Chrome(service=ChromeService(driver_path), options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if user_agent:
            options.set_preference("general.useragent.override", user_agent)
        return webdriver.Firefox(service=FirefoxService(driver_path), options=options)

    elif browser == "edge":
        options = EdgeOptions()
        if user_agent:
            options.add_argument(f"user-agent={user_agent}")
        return webdriver.Edge(service=EdgeService(driver_path), options=options)

    else:
        print("[X] Unsupported browser at runtime.")
        sys.exit(1)

# === Main Execution ===
url, browser, driver_path, user_agent, cookies = get_user_inputs()
driver = launch_driver(browser, driver_path, user_agent)

driver.get(url)
time.sleep(5)

if cookies:
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"[!] Cookie error: {e}")
    driver.refresh()
    time.sleep(5)

try:
    button = driver.find_element(By.XPATH, "//button[contains(@class, 'bg-green') or contains(text(), 'Download')]")
    button.click()
    print("[✓] Download triggered.")
    time.sleep(10)
except Exception as e:
    print(f"[X] Failed to click download: {e}")

finally:
    driver.quit()
