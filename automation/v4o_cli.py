import argparse
import os
import sys
import subprocess
import platform
import zipfile
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request

def install_missing_packages():
    try:
        import selenium
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium'])

install_missing_packages()

BROWSER_DRIVERS = {
    "chrome": {
        "url": "https://storage.googleapis.com/chrome-for-testing-public/latest/{platform}/chromedriver-{platform}.zip",
        "exec": "chromedriver"
    },
    "firefox": {
        "url": "https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-{platform}.zip",
        "exec": "geckodriver"
    },
    "edge": {
        "url": "https://msedgedriver.azureedge.net/LATEST_RELEASE",
        "exec": "msedgedriver"
    }
}

PLATFORM_MAP = {
    "Windows": "win64",
    "Linux": "linux64",
    "Darwin": "mac-arm64" if platform.machine() == "arm64" else "mac-x64"
}

def download_driver(browser: str):
    platform_key = PLATFORM_MAP[platform.system()]
    driver_info = BROWSER_DRIVERS[browser]
    url = driver_info['url'].format(platform=platform_key) if '{platform}' in driver_info['url'] else driver_info['url']
    zip_name = f"{driver_info['exec']}.zip"

    if not os.path.exists(driver_info['exec']):
        print(f"Downloading {browser} driver...")
        if browser == "edge":
            latest_url = urllib.request.urlopen(driver_info['url']).read().decode().strip()
            url = f"https://msedgedriver.azureedge.net/{latest_url}/edgedriver_{platform_key}.zip"
        urllib.request.urlretrieve(url, zip_name)
        with zipfile.ZipFile(zip_name, 'r') as zip_ref:
            zip_ref.extractall('.')
        os.remove(zip_name)
        print(f"{browser.capitalize()} driver installed.")
    return os.path.abspath(driver_info['exec'])

def setup_driver(browser: str, headless: bool, user_agent: str, driver_path: str):
    options = None
    if browser == "chrome":
        options = ChromeOptions()
    elif browser == "firefox":
        options = FirefoxOptions()
    elif browser == "edge":
        options = EdgeOptions()

    if headless:
        options.add_argument("--headless")
    if user_agent:
        options.add_argument(f"--user-agent={user_agent}")

    if browser == "chrome":
        return webdriver.Chrome(executable_path=driver_path, options=options)
    elif browser == "firefox":
        return webdriver.Firefox(executable_path=driver_path, options=options)
    elif browser == "edge":
        return webdriver.Edge(executable_path=driver_path, options=options)

def inject_cookies(driver, cookie_file, url):
    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
    driver.get(url)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(url)

def main():
    parser = argparse.ArgumentParser(description="Limewire Downloader Automation")
    parser.add_argument('--url', required=True, help='Target Limewire URL')
    parser.add_argument('--browser', default='chrome', choices=['chrome', 'firefox', 'edge'], help='Browser to use')
    parser.add_argument('--driver', help='Path to browser driver')
    parser.add_argument('--user-agent', help='Custom User-Agent string')
    parser.add_argument('--cookies', help='Path to cookies JSON file')
    parser.add_argument('--headless', default=action='store_true', help='Enable headless mode')
    args = parser.parse_args()

    driver_path = args.driver or download_driver(args.browser)
    driver = setup_driver(args.browser, args.headless, args.user_agent, driver_path)

    if args.cookies:
        inject_cookies(driver, args.cookies, args.url)
    else:
        driver.get(args.url)

    wait = WebDriverWait(driver, 20)
    try:
        green_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "green") or contains(@style, "green")]')))
        green_button.click()
        print("✅ Download button clicked successfully.")
    except Exception as e:
        print(f"❌ Could not find or click the download button: {e}")

    driver.quit()

if __name__ == "__main__":
    main()
