# Limewire Downloader - Automated Script (Cross-platform)

## ✅ Features

- Automatically downloads files from LimeWire shared links
- Works across **Windows**, **Linux**, and **macOS**
- Supports **Chrome**, **Firefox**, and **Edge** browsers
- Auto-downloads WebDrivers (ChromeDriver, GeckoDriver, EdgeDriver)
- Handles headless mode
- Optional **user-agent** override
- Optional **cookie injection** (for authenticated sessions)
- **CLI mode** with `argparse` support (no prompts)

---

## 🔧 Setup & Usage

### Requirements (installed automatically if missing)

- Python 3.6+
- `selenium`

---

## 🚀 How to Run (CLI Mode)

### Example:

```bash
python limewire_downloader_cli.py \
  --url "https://www.limewire.com/download/file123" \
  --browser chrome \
  --headless \
  --user-agent "CustomUserAgent/1.0" \
  --cookies cookies.json
```

### Arguments:

| Argument         | Description |
|------------------|-------------|
| `--url`          | Target LimeWire URL (required) |
| `--browser`      | Browser: `chrome`, `firefox`, or `edge` (default: chrome) |
| `--driver`       | Path to browser driver. If omitted, downloads automatically |
| `--user-agent`   | Custom User-Agent string (optional) |
| `--cookies`      | Path to JSON file with cookies (optional) |
| `--headless`     | Run browser in headless mode |

---

## 🧠 Optional Features

### 🛠 User-Agent Spoofing

Paste a custom user-agent string via `--user-agent`.

### 🍪 Cookie Injection

Provide a `.json` file like:

```json
[
  {"name": "sessionid", "value": "abc123", "domain": ".limewire.com"}
]
```

Use it via `--cookies cookies.json`.

---

## 🌐 Driver Installation Details

The script auto-detects your OS and browser. If the driver is not found:
- Downloads directly from official sources
- Extracts it into the current directory

Supported Drivers:
- **Chrome**: `chromedriver`
- **Firefox**: `geckodriver`
- **Edge**: `msedgedriver`

You can also manually provide driver path with `--driver`.

---

## 📂 Directory Structure

```
project-folder/
├── limewire_downloader_cli.py     # CLI automation script
├── chromedriver / geckodriver / msedgedriver  # Auto-downloaded browser drivers
├── cookies.json (optional)       # Cookie file
├── README_LimewireDownloader.md  # This file
```

---

## ❗ Notes

- Make sure the browser (Chrome, Firefox, Edge) is installed
- Script supports both interactive and non-interactive environments
- Antivirus/firewall may block downloads — allow exceptions if needed

---

## ✅ Upcoming Support

- Download resume & progress feedback
- GUI front-end version
- Proxy support & login helpers

---

## 🤝 Contributing

Raise a PR or open an issue to add browser support or other enhancements

---

## 📜 License

MIT License

---

Created with ❤️ by [Automation Assistant]
