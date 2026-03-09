# VTU Results Scraper 📊

A Python automation tool that collects **VTU semester results for an entire class** directly from the official results portal and exports them into a **clean, structured Excel sheet**.

Instead of manually checking each student's result one by one, this script automates the process while still respecting the CAPTCHA requirement.

---

# ✨ Features

* 🔎 Automatically fetch results for multiple USNs
* 📄 Clean, structured Excel output
* 🧩 Handles **PEC and OEC electives correctly**
* 🧹 Ignores backlog subjects automatically
* 📊 Organized subject grouping (Internals / Externals / Total / Result)
* ⚡ Fast (entire class results in a few minutes)

---


# ⚙️ How It Works

1. The script loads a list of **USNs from an Excel file**
2. Opens the VTU results portal automatically
3. Enters each USN
4. Waits for the user to solve the CAPTCHA
5. Scrapes the result page
6. Extracts the first **6 semester subjects only**
7. Categorizes electives as **PEC or OEC**
8. Writes results into a formatted Excel sheet

---

# 🧰 Requirements

Install Python dependencies:

```bash
pip install selenium pandas openpyxl beautifulsoup4
```

You will also need:

* **Python 3.8+**
* **Google Chrome**
* **ChromeDriver** (matching your Chrome version)

Download ChromeDriver:
https://chromedriver.chromium.org/downloads

Place the driver in the same folder as the script or ensure it is available in your system PATH.

---

# 📂 Project Structure

```
VTU-Results-Scraper
│
├── main.py
├── usn_list.xlsx
├── vtu_results.xlsx (generated after running)
└── README.md
```

---

# 📝 Preparing the Input File

Create an Excel file named:

```
usn_list.xlsx
```

Structure:

| USN        |
| ---------- |
| 1XX22XX001 |
| 1XX22XX002 |
| 1XX22XX003 |

Only one column is required.

---

# ▶️ Running the Script

Run the script using:

```bash
python main.py
```

The workflow will look like this:

```
Script enters USN
↓
You type CAPTCHA in the browser
↓
Press Submit
↓
Script scrapes results
↓
Script reloads page
↓
Next USN
```

Repeat until all students are processed.

---

# ⏱ Runtime

Approximate runtime for a class:

| Students | Time        |
| -------- | ----------- |
| 10       | ~40 seconds |
| 50       | ~3 minutes  |
| 70       | ~4 minutes  |

---

# 🧠 How Electives Are Handled

The VTU portal sorts subjects **by subject code**, which may mix PEC and OEC ordering.

This scraper solves that by classifying subjects based on their **subject code patterns**, ensuring:

```
PEC subjects → grouped under PEC
OEC subjects → grouped under OEC
```

This prevents incorrect swapping of elective results.

---

# ⚠️ CAPTCHA Notice

The VTU portal requires CAPTCHA verification for each request.

This tool **does not bypass CAPTCHA**.

You must manually enter the CAPTCHA for each student.

---

# 📌 Limitations

* Designed specifically for the **VTU results portal layout**
* Assumes **6 subjects per semester**
* Requires manual CAPTCHA entry
* Website layout changes may require script updates

---


# 🤝 Contributing

Pull requests are welcome.

If you find issues due to changes in the VTU portal layout, feel free to submit fixes or improvements.

---


# ⭐ If this helped you

Give the repository a star so other VTU students can find it easily!
