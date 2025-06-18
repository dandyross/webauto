import os
import subprocess
import sys
import time
import platform
import urllib.request

REQUIRED_MODULES = ["selenium"]


def install_missing_packages():
    for package in REQUIRED_MODULES:
        try:
            __import__(package)
        except ImportError:
            print(f"[!] '{package}' not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def download_chromedriver():
    system = platform.system()
    arch = platform.machine()

    if system == "Windows":
        zip_url = "https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111/win64/chromedriver-win64.zip"
        zip_name = "chromedriver.zip"
        driver_exe = "chromedriver.exe"
    elif system == "Linux":
        zip_url = "https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111/linux64/chromedriver-linux64.zip"
        zip_name = "chromedriver.zip"
        driver_exe = "chromedriver"
    elif system == "Darwin":
        zip_url = "https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111/mac-arm64/chromedriver-mac-arm64.zip"
        zip_name = "chromedriver.zip"
        driver_exe = "chromedriver"
    else:
        print("[X] Unsupported OS. Please install ChromeDriver manually.")
        sys.exit(1)

    print(f"[~] Downloading ChromeDriver for {system}...")
    urllib.request.urlretrieve(zip_url, zip_name)

    print("[~] Extracting driver...")
    import zipfile
    with zipfile.ZipFile(zip_name, 'r') as zip_ref:
        zip_ref.extractall()

    # Move to current dir
    for root, dirs, files in os.walk("."):
        if driver_exe in files:
            full_path = os.path.join(root, driver_exe)
            os.rename(full_path, os.path.join(os.getcwd(), driver_exe))
            break

    os.remove(zip_name)
    print("[✓] ChromeDriver installed in current directory.")
    return os.path.join(os.getcwd(), driver_exe)


def get_user_inputs():
    url = input("Enter the target LimeWire URL: ").strip()

    chromedriver_path = os.path.join(os.getcwd(), "chromedriver")
    if not os.path.exists(chromedriver_path):
        print("[!] ChromeDriver not found in current directory.")
        choice = input("Do you want to download and install it here? (y/n): ").strip().lower()
        if choice == 'y':
            chromedriver_path = download_chromedriver()
        else:
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
options.add_argument('--headless')

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

''' 
prommpts used
can  you please write an web automation coed inn py for instant deployment purpose . i want you press download button which is in green color as shown inn figure below. 
[media pointer="file-service://file-8cU6ZzpFLWapgiCYQaugqz"] webite screen shot
your are a senior expert in web automation 
can  you please write an web automation coed inn py for instant deployment purpose . i want you press download button which is in green color as shown inn figure below. 
write the code for nessary requriment file and run alnong with the main file and check if the nessary moduls are there in the current dir wjhere the main py is there ,,if not try install it and run the code

ps : 1)this code may run on terminal only subsystem where there is a posssiblityy of not even having the basics modules 
2)also add an optioon for giving the target url for runninh dynamically and if posssible make sure the chrome or othere browser drivers are in the same dir else allow the user the option to add it dynamically when running the main file , 
3) also write a dcumentation on how to use this file
all good  and yes but after adding whether to install the chrome driver to the curr dir  if the file is missing 
for all platforms and yes include the driver and 
optional :
1)can you make this for other browsers as well 
2)and  add option for add userageunt and add cookies as well
'''