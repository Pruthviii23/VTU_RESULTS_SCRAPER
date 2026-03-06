import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.styles import Alignment

# =============================
# Load USN list
# =============================

df = pd.read_excel("usn_list.xlsx")
usn_list = df["USN"].tolist()

# =============================
# Start browser
# =============================

driver = webdriver.Chrome()
wait = WebDriverWait(driver,120)

driver.get("https://results.vtu.ac.in/D25J26Ecbcs/index.php")

all_students = []

# =============================
# Scraping Loop
# =============================

for i,usn in enumerate(usn_list,1):

    print(f"\nProcessing {i}/{len(usn_list)} : {usn}")

    usn_box = wait.until(EC.presence_of_element_located((By.NAME,"lns")))
    usn_box.clear()
    usn_box.send_keys(usn)

    print("Enter captcha and press submit")

    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"divTableRow")))

    soup = BeautifulSoup(driver.page_source,"html.parser")

    student_data = {}

    try:

        # -------------------------
        # Extract Name + USN
        # -------------------------

        rows = soup.find_all("tr")

        for r in rows:

            if "Student Name" in r.text:
                tds = r.find_all("td")
                student_data["Name"] = tds[1].text.replace(":","").strip()

            if "University Seat Number" in r.text:
                tds = r.find_all("td")
                student_data["USN"] = tds[1].text.replace(":","").strip()

        # -------------------------
        # Extract Subject Rows
        # -------------------------

        subject_rows = soup.find_all("div",class_="divTableRow")[1:7]

        core_subject_codes = ["BAI701","BAI702","BAD703","BAI786"]

        for idx,row in enumerate(subject_rows):

            cells = row.find_all("div",class_="divTableCell")

            subject_code = cells[0].text.strip()
            subject_name = cells[1].text.strip()
            internal = cells[2].text.strip()
            external = cells[3].text.strip()
            total = cells[4].text.strip()
            result = cells[5].text.strip()

            # Core subjects
            if idx < 4:

                sub = core_subject_codes[idx]

                student_data[f"{sub}_Internal"] = internal
                student_data[f"{sub}_External"] = external
                student_data[f"{sub}_Total"] = total
                student_data[f"{sub}_Result"] = result

            else:

                # detect PEC vs OEC based on subject code
                if subject_code.startswith("BAD714C"):
                    student_data["PEC_Subject"] = subject_name
                    student_data["PEC_Internal"] = internal
                    student_data["PEC_External"] = external
                    student_data["PEC_Total"] = total
                    student_data["PEC_Result"] = result

                else:

                    student_data["OEC_Subject"] = subject_name
                    student_data["OEC_Internal"] = internal
                    student_data["OEC_External"] = external
                    student_data["OEC_Total"] = total
                    student_data["OEC_Result"] = result


        all_students.append(student_data)

        print("Scraped successfully")

    except Exception as e:
        print("Scrape error:",e)

    # reload search page for next student
    driver.get("https://results.vtu.ac.in/D25J26Ecbcs/index.php")
    time.sleep(2)

driver.quit()

# =============================
# Excel Creation
# =============================

wb = Workbook()
ws = wb.active

# Main headers
ws.cell(row=1,column=1,value="Name")
ws.cell(row=1,column=2,value="USN")

col = 3

core_subjects = ["BAI701","BAI702","BAD703","BAI786"]

# Core subjects headers
for sub in core_subjects:

    ws.merge_cells(start_row=1,start_column=col,end_row=1,end_column=col+3)
    ws.cell(row=1,column=col,value=sub)

    ws.cell(row=2,column=col,value="Internals")
    ws.cell(row=2,column=col+1,value="Externals")
    ws.cell(row=2,column=col+2,value="Total")
    ws.cell(row=2,column=col+3,value="Result")

    col += 4

# PEC header
ws.merge_cells(start_row=1,start_column=col,end_row=1,end_column=col+4)
ws.cell(row=1,column=col,value="PEC")

ws.cell(row=2,column=col,value="Subject")
ws.cell(row=2,column=col+1,value="Internals")
ws.cell(row=2,column=col+2,value="Externals")
ws.cell(row=2,column=col+3,value="Total")
ws.cell(row=2,column=col+4,value="Result")

col += 5

# OEC header
ws.merge_cells(start_row=1,start_column=col,end_row=1,end_column=col+4)
ws.cell(row=1,column=col,value="OEC")

ws.cell(row=2,column=col,value="Subject")
ws.cell(row=2,column=col+1,value="Internals")
ws.cell(row=2,column=col+2,value="Externals")
ws.cell(row=2,column=col+3,value="Total")
ws.cell(row=2,column=col+4,value="Result")

# =============================
# Fill Student Data
# =============================

row_num = 3

for student in all_students:

    ws.cell(row=row_num,column=1,value=student.get("Name",""))
    ws.cell(row=row_num,column=2,value=student.get("USN",""))

    col = 3

    for sub in core_subjects:

        ws.cell(row=row_num,column=col,value=student.get(f"{sub}_Internal",""))
        ws.cell(row=row_num,column=col+1,value=student.get(f"{sub}_External",""))
        ws.cell(row=row_num,column=col+2,value=student.get(f"{sub}_Total",""))
        ws.cell(row=row_num,column=col+3,value=student.get(f"{sub}_Result",""))

        col += 4

    # PEC
    ws.cell(row=row_num,column=col,value=student.get("PEC_Subject",""))
    ws.cell(row=row_num,column=col+1,value=student.get("PEC_Internal",""))
    ws.cell(row=row_num,column=col+2,value=student.get("PEC_External",""))
    ws.cell(row=row_num,column=col+3,value=student.get("PEC_Total",""))
    ws.cell(row=row_num,column=col+4,value=student.get("PEC_Result",""))

    col += 5

    # OEC
    ws.cell(row=row_num,column=col,value=student.get("OEC_Subject",""))
    ws.cell(row=row_num,column=col+1,value=student.get("OEC_Internal",""))
    ws.cell(row=row_num,column=col+2,value=student.get("OEC_External",""))
    ws.cell(row=row_num,column=col+3,value=student.get("OEC_Total",""))
    ws.cell(row=row_num,column=col+4,value=student.get("OEC_Result",""))

    row_num += 1

# Center headers
for cell in ws[1]:
    cell.alignment = Alignment(horizontal="center")

wb.save("vtu_results.xlsx")

print("\nExcel file created: vtu_results.xlsx")