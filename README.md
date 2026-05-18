# 📊 VTU Results Scraper (Auto CAPTCHA Version)

A fully automated Python tool that fetches VTU semester results for an entire class — including **automatic CAPTCHA solving using OCR** — and exports everything into a clean Excel sheet.

No manual input required.

---

# 🚀 What This Tool Does

* Takes a list of USNs (student IDs)
* Opens the VTU results website
* Automatically solves CAPTCHA using OCR
* Retries until correct CAPTCHA is found
* Scrapes student results
* Saves everything into a structured Excel file

---

# ✨ Features

* 🤖 **Automatic CAPTCHA solving (OCR-based)**
* 🔁 Smart retry system until success
* 🔎 Bulk result fetching for multiple students
* 📄 Clean Excel output
* 🧩 Correct PEC / OEC classification
* 🧹 Ignores backlog subjects automatically
* 📊 Structured marks (Internals / Externals / Total / Result)
* ⚡ Fully automated (no human input needed)

---

# ⚠️ Important Notice

This tool interacts with a live university website.

👉 Use responsibly:

* Avoid excessive requests
* Add delays if needed
* Do not overload the server

---

# 🧰 Requirements

## 1. Install Python

* Python **3.8 or above**
* Enable **“Add Python to PATH”**

---

## 2. Install Required Libraries

Run:

```bash
pip install selenium pandas openpyxl beautifulsoup4 easyocr opencv-python pillow
```

---

## 3. Install Google Chrome

Download and install Chrome if not already installed.

---

## 4. Install ChromeDriver

### Steps:

1. Check Chrome version:

```
chrome://settings/help
```

2. Download matching version:
   [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

3. Place `chromedriver.exe`:

* In project folder OR
* Add to system PATH

---

# 📂 Project Structure

```
VTU-Results-Scraper/
│
├── main.py
├── usn_list.xlsx
├── vtu_results.xlsx (generated)
├── dataset/              # (optional) saved captcha data
└── README.md
```

---

# 📝 Step 1: Prepare Input File

Create:

```
usn_list.xlsx
```

Format:

| USN        |
| ---------- |
| 1XX22XX001 |
| 1XX22XX002 |
| 1XX22XX003 |

👉 Only one column required
👉 Column name must be **USN**

---

# ▶️ Step 2: Run the Script

```
python main.py
```

---

# ⚙️ How It Works (Behind the Scenes)

For each student:

```
Enter USN
↓
Capture CAPTCHA image
↓
Preprocess image (OpenCV)
↓
Run OCR (EasyOCR)
↓
Submit prediction
↓
If wrong → retry automatically
↓
If correct → scrape results
↓
Move to next student
```

---

# 🔁 CAPTCHA Solver Logic

* Uses **image preprocessing + OCR**
* Filters invalid predictions
* Automatically retries until success
* No manual intervention required

---

# ⏱ Estimated Runtime

| Students | Time          |
| -------- | ------------- |
| 10       | ~1–2 minutes  |
| 50       | ~5–8 minutes  |
| 70       | ~8–12 minutes |

👉 Depends on OCR success rate (~20–40%)

---

# 🧠 How Electives Are Handled

VTU may mix subject order.

This script correctly classifies:

* **PEC (Program Elective)**
* **OEC (Open Elective)**

Based on subject codes → ensuring correct grouping.

---

# 📊 Output

Generated file:

```
vtu_results.xlsx
```

Includes:

* Name
* USN
* Core subjects (Internals / Externals / Total / Result)
* PEC subject + marks
* OEC subject + marks

---

# ⚠️ Limitations

* CAPTCHA solver is not perfect (OCR-based)
* May retry multiple times before success
* Depends on current VTU site structure
* Website changes may break script

---

# 💡 Tips for Better Performance

* Keep system idle while running
* Use good internet connection
* Avoid running too many instances
* If blocked → wait and retry later

---

# 🤝 Contributing

Feel free to:

* Improve CAPTCHA accuracy
* Optimize speed
* Handle new VTU layouts

Pull requests are welcome.

---

# ⭐ If This Helped You

Give the repo a star ⭐
Helps other VTU students discover it.
* Or a **resume bullet that actually stands out**
* Or even turn this into a **mini AI project (custom captcha model)**
