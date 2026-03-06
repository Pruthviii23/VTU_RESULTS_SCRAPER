import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

df = pd.read_excel("usn_list.xlsx")
usn_list = df["USN"].tolist()

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 120)

driver.get("https://results.vtu.ac.in/D25J26Ecbcs/index.php")

results = []

for usn in usn_list:

    print(f"\nProcessing {usn}")

    usn_box = wait.until(EC.presence_of_element_located((By.NAME, "lns")))
    usn_box.clear()
    usn_box.send_keys(usn)

    print("Enter captcha and press SUBMIT")

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "divTableRow")))

    soup = BeautifulSoup(driver.page_source, "html.parser")

    try:

        # find student name row
        student_name = None
        rows = soup.find_all("tr")

        for row in rows:
            if "Student Name" in row.text:
                tds = row.find_all("td")
                student_name = tds[1].text.replace(":", "").strip()

        if student_name is None:
            raise Exception("Name not found")

        subject_rows = soup.find_all("div", class_="divTableRow")

        for row in subject_rows[1:]:

            cells = row.find_all("div", class_="divTableCell")

            if len(cells) < 6:
                continue

            results.append({
                "USN": usn,
                "Name": student_name,
                "Subject Code": cells[0].text.strip(),
                "Subject Name": cells[1].text.strip(),
                "Internal": cells[2].text.strip(),
                "External": cells[3].text.strip(),
                "Total": cells[4].text.strip(),
                "Result": cells[5].text.strip()
            })

        print("Scraped successfully")

    except Exception as e:
        print("Scraping error:", e)

    driver.get("https://results.vtu.ac.in/D25J26Ecbcs/index.php")
    time.sleep(2)

output_df = pd.DataFrame(results)
output_df.to_excel("vtu_results.xlsx", index=False)

print("Saved to vtu_results.xlsx")

driver.quit()