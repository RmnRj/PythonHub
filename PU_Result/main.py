import time # Used for adding delays (e.g., time.sleep)
import json # Used for working with JSON data (saving results to a .json file)
import sys # Provides access to system-specific parameters and functions (e.g., sys.stdout.reconfigure)
import re # Used for regular expressions, useful for pattern matching in text

from selenium import webdriver # The main Selenium library to interact with web browsers
from selenium.webdriver.common.by import By # Used to specify how to locate elements (e.g., by ID, by CSS selector)
from selenium.webdriver.support.ui import Select, WebDriverWait # Select for dropdowns, WebDriverWait for explicit waits
from selenium.webdriver.support import expected_conditions as EC # Conditions used with WebDriverWait (e.g., element to be clickable)
from selenium.webdriver.chrome.service import Service as ChromeService # Service object for ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager # Automatically manages (downloads/updates) ChromeDriver executable

# Reconfigure standard output to use UTF-8 encoding, important for non-ASCII characters (like Nepali names)
sys.stdout.reconfigure(encoding='utf-8')

# --- Configuration ---
# Define the starting and ending roll numbers for the scraping range
start_roll = 21075049
end_roll = 21075089
# Define the date of birth to be used for all form submissions
dob = "2005-02-08" # Your date of birth for the form


# --- Selenium Setup ---
# Attempt to initialize the Chrome WebDriver
try:
    # Use ChromeDriverManager to automatically download and configure the correct ChromeDriver
    service = ChromeService(executable_path=ChromeDriverManager().install())
    # Initialize the Chrome browser instance
    driver = webdriver.Chrome(service=service)
except Exception as e:
    # If WebDriver initialization fails, print an error and exit the script
    print(f"Error initializing WebDriver: {e}")
    print("Please ensure you have Chrome installed and a stable internet connection for ChromeDriver download.")
    sys.exit(1) # Terminate the script

# Maximize the browser window for better visibility and to avoid layout issues
driver.maximize_window()
# Initialize an empty list to store the results for all students
results = [] 

print(f"Starting to scrape results from Roll No. {start_roll} to {end_roll}...")

# Loop through each roll number in the specified range
for roll in range(start_roll, end_roll + 1):
    # Initialize a dictionary for the current student's data with default values
    student_data = {
        "name": None, # Student's name, will be extracted
        "exam_roll": roll, # The current roll number being processed
        "courses": [], # List to store extracted course details
        "sgpa": None, # SGPA value, will be extracted
        "status": "Processing..." # Status of the extraction for this roll number
    }
    
    try:
        print(f"\nProcessing Roll No: {roll}")
        # Navigate to the result submission form URL
        driver.get("https://exam.pu.edu.np:9094")

        # Wait up to 10 seconds for the "Year" input element to be present on the page
        # This ensures the page is sufficiently loaded before interacting with elements
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Year")))

        # Fill out the form fields using their respective IDs
        driver.find_element(By.ID, "Year").send_keys("2024") # Input for the year
        # Select dropdown options by their visible text
        Select(driver.find_element(By.ID, "Academic_System")).select_by_visible_text("Fall")
        # Select dropdown options by their index (0-based)
        Select(driver.find_element(By.ID, "Semester")).select_by_index(6) 
        Select(driver.find_element(By.ID, "Exam_Type")).select_by_visible_text("Regular/Retake")
        Select(driver.find_element(By.ID, "Program")).select_by_visible_text("Bachelor of Computer Engineering")
        # Input the current roll number into the "Symbol_Number" field
        driver.find_element(By.ID, "Symbol_Number").send_keys(str(roll))
        # Input the defined date of birth into the "DOB" field
        driver.find_element(By.ID, "DOB").send_keys(dob)

        # Wait up to 10 seconds for the submit button to be clickable
        submit = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']")) # Locates the submit button by its CSS selector
        )
        # Scroll the submit button into view if it's not currently visible (can prevent click issues)
        driver.execute_script("arguments[0].scrollIntoView(true);", submit)
        # Click the submit button to submit the form
        submit.click()

        # IMPORTANT: Pause execution for 3 seconds to allow the new page/results to load
        # This is crucial for dynamic content or page navigation after submission.
        time.sleep(3) 

        # --- Extracting information from the loaded page ---
        # Get the complete HTML source of the page after all dynamic content has loaded
        page_source = driver.page_source
        # Initialize BeautifulSoup to parse the HTML source
        from bs4 import BeautifulSoup 
        soup = BeautifulSoup(page_source, 'html.parser')

        # 1. Extract Student Name
        try:
            # Find the <strong> tag that contains the text "Student Name:" (case-insensitive)
            name_strong_tag = soup.find('strong', string=re.compile(r'Student Name:', re.IGNORECASE))
            if name_strong_tag:
                # The student's name is typically the direct text sibling (NavigableString) of the <strong> tag
                student_name_text = name_strong_tag.next_sibling
                if student_name_text:
                    # Clean up the extracted text: remove leading/trailing whitespace and any surrounding quotes
                    student_data["name"] = student_name_text.strip().strip('"') 
                    # print(f"  Student Name: {student_data['name']}") # Uncomment for detailed console output
                else:
                    print(f"  Warning: Student Name label found for {roll}, but no name text followed.")
            else:
                print(f"  Warning: 'Student Name:' label not found on the page for {roll}.")
        except Exception as e:
            print(f"  Error extracting Student Name for {roll}: {e}")

        # 2. Extract Course Details from the table
        try:
            # Find the first <tbody> element in the HTML, which usually contains table data rows
            tbody = soup.find('tbody') 
            if tbody:
                # Find all table row (<tr>) elements within the <tbody>
                rows = tbody.find_all('tr')
                
                # Iterate through each row to extract course information
                for i, row in enumerate(rows):
                    # Find all table data (<td>) cells within the current row
                    cols = row.find_all('td')
                    
                    # Criteria to identify a valid course data row:
                    # - Must have at least 5 columns (S.No, Code, Title, Credit, Grade, Remarks)
                    # - Must NOT contain "Total" or "SGPA =" in its text (to exclude summary rows)
                    row_text = row.get_text(strip=True)
                    if len(cols) >= 5 and "Total" not in row_text and "SGPA =" not in row_text:
                        # Extract data from specific column indices (0-based)
                        # Based on your table image:
                        # cols[1] -> Code No.
                        # cols[2] -> Course Title
                        # cols[4] -> Grade
                        subject_code = cols[1].get_text(strip=True)
                        subject_name = cols[2].get_text(strip=True)
                        grade = cols[4].get_text(strip=True)
                        
                        # Append the extracted course details as a dictionary to the 'courses' list
                        student_data["courses"].append({
                            "code": subject_code, 
                            "title": subject_name,
                            "grade": grade
                        })
                        # print(f"    Course: {subject_code} - {subject_name}, Grade: {grade}") # Uncomment for debugging course extraction
            else:
                print(f"  Warning: Course table (tbody) not found for {roll}.")
        except Exception as e:
            print(f"  Error extracting courses for {roll}: {e}")

        # 3. Extract SGPA
        try:
            # Find the <td> tag that contains the text "SGPA =" (case-insensitive)
            sgpa_td = soup.find('td', string=re.compile(r'SGPA\s*=', re.IGNORECASE))
            if sgpa_td:
                sgpa_text = sgpa_td.get_text(strip=True)
                # Use regex to extract the value that comes after "SGPA = "
                sgpa_value_match = re.search(r'SGPA\s*=\s*(.*)', sgpa_text, re.IGNORECASE)
                if sgpa_value_match:
                    sgpa_text = sgpa_value_match.group(1).strip()
                    student_data["sgpa"] = sgpa_text# Capture group 1 is the value
                    print(f"  SGPA: {student_data['sgpa']}")
                    if sgpa_text == "-":
                        student_data["status"] = "Fail" # Set status to Fail
                    elif sgpa_text != "-" and sgpa_text is not None: # A != None [this is also correct]
                        student_data["status"] = "Pass"
                else:
                    print(f"  Warning: SGPA label found for {roll}, but value could not be extracted.")
                    student_data["status"] = "value could not be extracted." # Indicate partial success
            else:
                print(f"  Warning: SGPA label not found on the page for {roll}.")
                student_data["status"] = "Dropout Student" # Indicate partial success
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
        # This block always executes, regardless of whether an error occurred or not.
        # It ensures that the data for the current student (even if incomplete or erroneous)
        # is appended to the results list.
        results.append(student_data)

# --- Finalization ---
driver.quit() # Close the Chrome browser instance after all roll numbers have been processed

# Save the collected results to a JSON file
try:
    # Open 'pu_results.json' in write mode, ensuring UTF-8 encoding for proper character handling
    with open("Result/pu_results.json", "w", encoding="utf-8") as f:
        # Dump the 'results' list into the JSON file
        # indent=2 makes the JSON output human-readable with 2-space indentation
        # ensure_ascii=False allows non-ASCII characters (like Nepali names) to be saved directly
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\nAll results saved to 'pu_results.json'")
except Exception as e:
    print(f"\nError saving results to JSON: {e}")