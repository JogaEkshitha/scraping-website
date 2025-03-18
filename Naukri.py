from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import numpy as np

# Define job roles & locations
job_roles = ["Full Stack Developer", "Data Analyst", "Software Engineer","python-developer","Degital Marketing","UI/UX Designer","Prodact Manager"]
locations = ["Bangalore", "Hyderabad", "Chennai","Pune","Mumbai","Delhi"]

# Set up WebDriver (Ensure chromedriver is in the project folder or provide full path)
driver = webdriver.Chrome()

# Create an empty list to store job data
job_data = []

for job in job_roles:
    for loc in locations:
        url = f"https://www.naukri.com/{job}-jobs-in-{loc}"
        driver.get(url)
        time.sleep(5)  # Allow time for the page to load
        
        while True:  # Loop through multiple pages
            job_cards = driver.find_elements(By.CLASS_NAME, 'cust-job-tuple')

            for job_card in job_cards:
                try:
                    title = job_card.find_element(By.CLASS_NAME, 'title').text
                    company = job_card.find_element(By.CLASS_NAME, 'comp-name').text
                    location = job_card.find_element(By.CLASS_NAME, 'locWdth').text
                    experience = job_card.find_element(By.CLASS_NAME, 'expwdth').text
                    salary = job_card.find_element(By.CLASS_NAME, 'sal').text if job_card.find_elements(By.CLASS_NAME, 'sal') else np.nan

                    job_data.append([title, company, location, experience, salary])
                    print(f"Scraped: {title} | {company} | {location} | {experience} | {salary}")

                except Exception as e:
                    print(f"Error: {e}")
                    continue

            # Check for "Next" button & go to the next page
            try:
                next_button = driver.find_element(By.XPATH, '//a[text()="Next"]')
                next_button.click()
                time.sleep(3)  # Wait for new page to load
            except:
                print("No more pages for:", job, loc)
                break  # Exit loop if no more pages

driver.quit()

# Convert to DataFrame
df = pd.DataFrame(job_data, columns=["Job Title", "Company", "Location", "Experience", "Salary"])

# Filter out rows where salary is "Not disclosed"
df = df[df["Salary"] != "Not disclosed"]

# Save data to CSV
output_file = "naukri_jobs.csv"
df.to_csv(output_file, index=False)
print("Data saved to naukri_jobs.csv ")