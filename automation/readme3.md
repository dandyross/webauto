# Limewire Downloader - Automated Script (Cross-platform)

## ✅ Features

* Automatically downloads files from LimeWire shared links
* Works across **Windows**, **Linux**, and **macOS**
* Supports **Chrome**, with extensible options for Firefox and Edge
* Auto-downloads WebDrivers (ChromeDriver, GeckoDriver, EdgeDriver)
* Handles headless mode
* Optional **user-agent** override
* Optional **cookie injection** (for authenticated sessions)

---

## 🔧 Setup & Usage

### Requirements (installed automatically if missing)

* Python 3.6+
* `selenium`

---

## 🚀 How to Run

### Step 1: Run the Script

```bash
python limewire_downloader.py
```

### Step 2: Input Prompts

You will be prompted to:

* Enter the LimeWire URL
* Choose or install browser WebDriver (ChromeDriver etc.)
* Optional: Provide a **custom User-Agent**
* Optional: Inject cookies (JSON format)

### Step 3: Script Actions

* Opens the LimeWire page
* Waits for content
* Locates the **green Download** button
* Clicks to initiate the download

---

## 🧠 Optional Features

### 🛠 User-Agent Spoofing

You can paste a custom user-agent string when prompted.

### 🍪 Cookie Injection

Useful for pages requiring login/session. Paste JSON cookie list like this when prompted:

```json
[
  {"name": "sessionid", "value": "abc123", "domain": "limewire.com"}
]
```

---

## 🌐 Driver Installation Details

The script auto-detects your platform and offers to download:

* **Chrome**: ChromeDriver
* **Firefox**: GeckoDriver
* **Edge**: EdgeDriver

Drivers are downloaded directly from official sources.

If you already have drivers, you may provide the path manually.

---

## 📂 Directory Structure

```
project-folder/
├── limewire_downloader.py  # Main automation script
├── chromedriver            # Auto-downloaded or user-provided driver
├── README_LimewireDownloader.md  # This file
```

---

## ❗ Notes

* Ensure Google Chrome (or respective browser) is installed
* Some antivirus/firewalls may block driver downloads
* Run in an environment with internet access

---

## ✅ Upcoming Support

*

---

## 🤝 Contributing

If you'd like support for other browsers or enhancements, raise a PR or open an issue.

---

## 📜 License

MIT License

---

Created with ❤️ by \[Automation Assistant]
