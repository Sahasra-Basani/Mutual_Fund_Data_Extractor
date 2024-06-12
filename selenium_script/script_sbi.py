from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import json
import os
import shutil
from process_date import DateDetails as Dd

# Get the previous month
prev_mon_name_MM = Dd.prev_mon_name_MM

# Get the current year four digits
current_year_yyyy = Dd.current_year_yyyy

# Get the days in the month
days_in_month = Dd.days_in_month
date = days_in_month+" "+prev_mon_name_MM+" "+str(current_year_yyyy)

with open("config.json") as f:
    config = json.load(f)

# Default download directory
default_download_path = config["other_settings"]["default_download_path"]

# Set the download directory
download_dir = config["other_settings"]["download_path_sbi"]

# Initialize the WebDriver
driver = webdriver.Chrome()
print("Chrome Driver Started")

# Url for the webpage
url = config["other_settings"]["url_sbi"]

# Load the webpage
driver.get(url)
print("URL launched")

time.sleep(5)

# Maximize the browser window
driver.maximize_window()

try:
    # Wait for the notification dialog to appear
    try:
        # Wait for maximum 10 seconds for the dialog to appear
        notification_dialog = WebDriverWait(driver, 10).until(ec.alert_is_present())

        # Switch to the alert
        alert = driver.switch_to.alert

        # Accept the alert (allow notifications)
        alert.dismiss()
        print("Show notification dialog is dismissed!!!")
        time.sleep(5)
    except:
        # If the dialog doesn't appear within 10 seconds, or if it's not an alert, continue without handling it
        pass

    # Find the element of dropdown
    year_dropdown = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "PSYear")))
    # Click on the select year dropdown
    year_dropdown.click()
    time.sleep(3)

    # Find the element of dropdown
    year_value = WebDriverWait(driver, 10).until(ec.presence_of_element_located(
        (By.XPATH, f"//div[@class='select-items']/div[contains(text(), '{current_year_yyyy}')]")))
    # Click on the current year
    year_value.click()
    print("Selected the year from the dropdown")
    time.sleep(3)

    # Find element of welcome notification
    welcome_notification = driver.find_element(By.XPATH, "//*[@id='notification-message-div']/div[2]/span")
    time.sleep(2)

    # Check whether the notification is available
    # If available then close it else select the month
    if welcome_notification:
        print("Notification exists-", welcome_notification.text)
        # Find the element of circle
        circle_element = driver.find_element(By.XPATH, "//div[@class='notification-message-hide-div notification"
                                                       "-message-hide-div-intent-bubble']")
        # Click on the element to exit the notification
        circle_element.click()
        print("Clicked on the notification exit circle")
        time.sleep(2)

    else:
        print("Notification does not exists.!!!")

    # Find the element of dropdown
    month_dropdown = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "PSMonth")))
    # Click on the select month dropdown
    month_dropdown.click()
    time.sleep(3)

    # Find the element of dropdown
    month_value = WebDriverWait(driver, 10).until(ec.presence_of_element_located(
        (By.XPATH, f"//div[@class='select-items']/div[contains(text(), '{prev_mon_name_MM}')]")))
    # Click on the previous month
    month_value.click()
    print("Selected the month from the dropdown")
    time.sleep(3)

    # Click on the link of file name to download
    download_file = driver.find_element(By.XPATH,
                                        f"//a[contains(text(), 'All Schemes Monthly Portfolio - as on {date}')]")

    # Get the list of files before downloading
    initial_files = os.listdir(default_download_path)

    # Click on the download link
    download_file.click()
    print("Clicked on the download files!!!")
    time.sleep(5)

    # Get the list of files after downloading
    final_files = os.listdir(default_download_path)

    # Find the new file
    new_file = list(set(final_files) - set(initial_files))[0]

    # Move the new file to the desired location
    source_file_path = os.path.join(default_download_path, new_file)
    destination_dir = download_dir
    # os.rename(source_file_path, os.path.join(destination_dir, new_file))
    shutil.move(source_file_path, os.path.join(destination_dir, new_file))

    print("File moved to the location successfully!!!")

finally:
    # Close the WebDriver
    driver.quit()
    print("Driver killed")


