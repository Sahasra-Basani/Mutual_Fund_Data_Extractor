from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import os
import shutil
import process_date

# Get the previous month
prev_mon_name_MM = process_date.prev_mon_name_MM
# Get the current year YYYY
current_year_yyyy = process_date.current_year_yyyy

with open("../config.json") as f:
    config = json.load(f)

# Default download directory
default_download_path = config["other_settings"]["default_download_path"]

# Set the download directory
download_dir = config["other_settings"]["download_path_nippon"]

# Initialize the WebDriver
driver = webdriver.Chrome()
print("Chrome Driver Started")

# Url for the webpage
url = config["other_settings"]["url_nippon"]

# Load the webpage
driver.get(url)
print("URL launched")

time.sleep(5)

# Maximize the browser window
driver.maximize_window()

try:
    time.sleep(5)

    # Find the label containing the desired text
    label_element = driver.find_element(By.XPATH,
                                        f"//label[contains(text(), 'Monthly portfolio for the month of {prev_mon_name_MM} {current_year_yyyy}')]")

    # Find the download link associated with the label
    download_link = label_element.find_element(By.XPATH,"../label/a[@class='xls']")

    time.sleep(5)

    # Get the list of files before downloading
    initial_files = os.listdir(default_download_path)

    # Click on the download link
    download_link.click()
    print("Clicked on the link to download the file")

    time.sleep(5)

    # Get the list of files after downloading
    final_files = os.listdir(default_download_path)

    # Find the new file
    new_file = list(set(final_files) - set(initial_files))[0]

    # Move the new file to the desired location
    source_file_path = os.path.join(default_download_path, new_file)
    destination_dir = download_dir
    shutil.move(source_file_path, os.path.join(destination_dir, new_file))

    print("File moved to the location successfully!!!")

finally:
    # Close the WebDriver
    driver.quit()
    print("Driver killed")


