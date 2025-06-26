import time 
import json 
import sys 
import re # Used for regular expressions, useful for pattern matching in text

from selenium import webdriver 
from selenium.webdriver.common.by import By # CSS selector
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService # Service object for ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager # Automatically manages (downloads/updates)

# Reconfigure standard output to use UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

start_roll = 21075049
end_roll = 21075089

dob = "2002-12-09" # Your date of birth for the form because DoB of PU result portal is useless

try:
    service = ChromeService(executable_path=ChromeDriverManager().install())
    # Initialize the Chrome browser 
    driver = webdriver.Chrome(service=service)
except Exception as e:
    print(f"Error initializing WebDriver: {e}")
    print("Please ensure you have Chrome installed and a stable internet connection for ChromeDriver download.")
    sys.exit(1) 


driver.maximize_window()
results = [] 

print(f"Starting to scrape results from Roll No. {start_roll} to {end_roll}...")


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

        # Wait up to 10 seconds for the submit button
        submit = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']")) 
        )
       
        driver.execute_script("arguments[0].scrollIntoView(true);", submit)
        # Click the submit button
        submit.click()

        
        time.sleep(3) 

        page_source = driver.page_source
       
        from bs4 import BeautifulSoup 
        soup = BeautifulSoup(page_source, 'html.parser')

      
        try:
            name_strong_tag = soup.find('strong', string=re.compile(r'Student Name:', re.IGNORECASE))
            if name_strong_tag:
                student_name_text = name_strong_tag.next_sibling
                if student_name_text:
                    student_data["name"] = student_name_text.strip().strip('"') 
                else:
                    print(f"  Warning: Student Name label found for {roll}, but no name text followed.")
            else:
                print(f"  Warning: 'Student Name:' label not found on the page for {roll}.")
        except Exception as e:
            print(f"  Error extracting Student Name for {roll}: {e}")

      
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
                        
                        # Append 
                        student_data["courses"].append({
                            "code": subject_code, 
                            "title": subject_name,
                            "grade": grade
                        })
                      
            else:
                print(f"  Warning: Course table (tbody) not found for {roll}.")
        except Exception as e:
            print(f"  Error extracting courses for {roll}: {e}")

        try:
            sgpa_td = soup.find('td', string=re.compile(r'SGPA\s*=', re.IGNORECASE))
            if sgpa_td:
                sgpa_text = sgpa_td.get_text(strip=True)
                
                sgpa_value_match = re.search(r'SGPA\s*=\s*(.*)', sgpa_text, re.IGNORECASE)
                if sgpa_value_match:
                    sgpa_text = sgpa_value_match.group(1).strip()
                    student_data["sgpa"] = sgpa_text # Capture group 1 is the value
                    print(f"  SGPA: {student_data['sgpa']}")
                    if sgpa_text == "-":
                        student_data["status"] = "Fail" # Set status to Fail
                    elif sgpa_text != "-" and sgpa_text is not None: 
                        student_data["status"] = "Pass"
                else:
                    print(f"  Warning: SGPA label found for {roll}, but value could not be extracted.")
                    student_data["status"] = "value could not be extracted." 
                print(f"  Warning: SGPA label not found on the page for {roll}.")
                student_data["status"] = "Dropout Student"
        except Exception as e:
            print(f"  Error extracting SGPA for {roll}: {e}")

        # If no specific status set by SGPA extraction, default to Success
        if student_data["status"] == "Processing...":
             student_data["status"] = "Success (SGPA not found)" # Covers cases where SGPA might genuinely not be there for some students

    except Exception as e:
        # Catch any general exceptions that might occur during the process for a given roll number
        student_data["status"] = f"Error: {e}"
        print(f"[!] Error processing Roll No. {roll}: {e}")
    finally:
        results.append(student_data)

driver.quit()

# Save the collected results 
try:
    with open("Result/pu_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\nAll results saved to 'pu_results.json'")
except Exception as e:
    print(f"\nError saving results to JSON: {e}")