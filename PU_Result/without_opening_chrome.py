import time
import json
import sys
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# --- HEADLESS MODE CHANGE: ADDED ---
from selenium.webdriver.chrome.options import Options 

sys.stdout.reconfigure(encoding='utf-8')

# --- Configuration ---
start_roll = 21075049
end_roll = 21075089
dob = "2005-02-08" # Your date of birth for the form


# --- Selenium Setup ---
try:
    # --- HEADLESS MODE CHANGE: ADDED ---
    # Create an Options object for Chrome to configure browser behavior
    chrome_options = Options()
    # --- HEADLESS MODE CHANGE: ADDED ---
    # Add the '--headless' argument to run the browser without a graphical user interface
    chrome_options.add_argument("--headless") 
    # --- HEADLESS MODE CHANGE: ADDED ---
    # Recommended argument for headless mode, especially on Windows, to avoid rendering issues
    chrome_options.add_argument("--disable-gpu") 
    # --- HEADLESS MODE CHANGE: ADDED ---
    # You can also add --window-size to ensure consistent rendering dimensions in headless mode
    # chrome_options.add_argument("--window-size=1920,1080")

    service = ChromeService(executable_path=ChromeDriverManager().install())
    # --- HEADLESS MODE CHANGE: MODIFIED ---
    # Initialize the Chrome browser instance, passing the 'options' object
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    print(f"Error initializing WebDriver: {e}")
    print("Please ensure you have Chrome installed and a stable internet connection for ChromeDriver download.")
    sys.exit(1)

# driver.maximize_window() # --- HEADLESS MODE CHANGE: NOTE ---
# In headless mode, maximizing the window has no visual effect and is less critical.
# The --window-size argument in ChromeOptions is more relevant for defining rendering dimensions.
driver.maximize_window() 
results = [] 

print(f"Starting to scrape results from Roll No. {start_roll} to {end_roll} (headless mode)...") # --- HEADLESS MODE CHANGE: MODIFIED ---
# Added " (headless mode)" to the print statement for clarity

for roll in range(start_roll, end_roll + 1):
    student_data = {
        "name": None,
        "exam_roll": roll,
        "courses": [],
        "sgpa": None,
        "status": "Processing..."
    }
    
    try:
        print(f"\nProcessing Roll No: {roll}")
        driver.get("https://exam.pu.edu.np:9094")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Year")))

        driver.find_element(By.ID, "Year").send_keys("2024")
        Select(driver.find_element(By.ID, "Academic_System")).select_by_visible_text("Fall")
        Select(driver.find_element(By.ID, "Semester")).select_by_index(6)
        Select(driver.find_element(By.ID, "Exam_Type")).select_by_visible_text("Regular/Retake")
        Select(driver.find_element(By.ID, "Program")).select_by_visible_text("Bachelor of Computer Engineering")
        driver.find_element(By.ID, "Symbol_Number").send_keys(str(roll))
        driver.find_element(By.ID, "DOB").send_keys(dob)

        submit = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", submit)
        submit.click()

        time.sleep(3) 

        page_source = driver.page_source
        from bs4 import BeautifulSoup 
        soup = BeautifulSoup(page_source, 'html.parser')

        # 1. Extract Student Name
        try:
            name_strong_tag = soup.find('strong', string=re.compile(r'Student Name:', re.IGNORECASE))
            if name_strong_tag:
                student_name_text = name_strong_tag.next_sibling
                if student_name_text:
                    student_data["name"] = student_name_text.strip().strip('"') 
                    print(f"  Student Name: {student_data['name']}")
                else:
                    print(f"  Warning: Student Name label found for {roll}, but no name text followed.")
            else:
                print(f"  Warning: 'Student Name:' label not found on the page for {roll}.")
        except Exception as e:
            print(f"  Error extracting Student Name for {roll}: {e}")

        # 2. Extract Course Details
        try:
            tbody = soup.find('tbody') 
            if tbody:
                rows = tbody.find_all('tr')
                
                for i, row in enumerate(rows):
                    cols = row.find_all('td')
                    
                    row_text = row.get_text(strip=True)
                    if len(cols) >= 5 and "Total" not in row_text and "SGPA =" not in row_text:
                        subject_code = cols[1].get_text(strip=True)
                        subject_name = cols[2].get_text(strip=True)
                        grade = cols[4].get_text(strip=True)
                        
                        student_data["courses"].append({
                            "code": subject_code, 
                            "title": subject_name,
                            "grade": grade
                        })
            else:
                print(f"  Warning: Course table (tbody) not found for {roll}.")
        except Exception as e:
            print(f"  Error extracting courses for {roll}: {e}")

        # 3. Extract SGPA
        try:
            sgpa_td = soup.find('td', string=re.compile(r'SGPA\s*=', re.IGNORECASE))
            if sgpa_td:
                sgpa_text = sgpa_td.get_text(strip=True)
                sgpa_value_match = re.search(r'SGPA\s*=\s*(.*)', sgpa_text, re.IGNORECASE)
                if sgpa_value_match:
                    sgpa_text = sgpa_value_match.group(1).strip()
                    student_data["sgpa"] = sgpa_text
                    print(f"  SGPA: {student_data['sgpa']}")
                    if sgpa_text == "-":
                        student_data["status"] = "Fail" # Set status to Fail
                    elif sgpa_text != "-" and student_data["sgpa"] is not None: # A != None [this is also correct]
                        student_data["status"] = "Pass"
                else:
                    print(f"  Warning: SGPA label found for {roll}, but value could not be extracted.")
                    student_data["status"] = "value could not be extracted."
            else:
                print(f"  Warning: SGPA label not found on the page for {roll}.")
                student_data["status"] = "Dropout Student"
        except Exception as e:
            print(f"  Error extracting SGPA for {roll}: {e}")

        if student_data["status"] == "Processing...":
             student_data["status"] = "Success (SGPA not found)" 

    except Exception as e:
        student_data["status"] = f"Error: {e}"
        print(f"[!] Error processing Roll No. {roll}: {e}")
    finally:
        results.append(student_data)

# --- Finalization ---
driver.quit() 

try:
    with open("Result/pu_results2.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\nAll results saved to 'pu_results.json'")
except Exception as e:
    print(f"\nError saving results to JSON: {e}")