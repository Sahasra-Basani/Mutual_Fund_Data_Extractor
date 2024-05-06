from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import json

with open("config.json") as f:
    config = json.load(f)

# Initialize the WebDriver
driver = webdriver.Chrome()
print("Chrome Driver Started")

# Url for the webpage
url = config["other_settings"]["url_hsbc"]

# Load the webpage
driver.get(url)
print("URL launched")

time.sleep(5)

# Maximize the browser window
driver.maximize_window()

#
# //*[@id="tabpanelinner-1797700734"]/div/div/div/table/tbody[2]/tr[40]/td[2]/span/strong/a
# //*[@id="tabpanelinner-1797700734"]/div/div/div/table/tbody[2]/tr[32]/td[2]/span/strong/a
# //*[@id="tabpanelinner-1797700734"]/div/div/div/table/tbody[2]/tr[24]/td[2]/span/strong/a
# //*[@id="tabpanelinner-1797700734"]/div/div/div/table/tbody[2]/tr[15]/td[2]/span/strong/a


# div = //*[@id="__tealiumGDPRecModal"]
# button = //*[@id="consent_prompt_submit"]
# //*[@id="terms-and-conditions-modal"]/div[3]/div/div[3]/a[2]

try:
    time.sleep(5)
    #
    # # Find the label containing the desired text
    # label_element = driver.find_element(By.XPATH,
    #                                     "//label[contains(text(), 'Monthly portfolio for the month of March 2024')]")

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
        print("Show notification dialog is not available!!!")

    # Click on the accept all cookies
    accept_cookies_link = driver.find_element(By.XPATH,"//*[@id='consent_prompt_submit']")

    time.sleep(5)
    accept_cookies_link.click()
    print("Clicked on the accept all cookies link")

    time.sleep(5)

    # Click on the accept all cookies
    accept_link = driver.find_element(By.XPATH, "//*[@id='terms-and-conditions-modal']/div[3]/div/div[3]/a[2]")

    time.sleep(5)
    accept_link.click()
    print("Clicked on the accept link")

    time.sleep(5)

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
        print("Show notification dialog is not available!!!")

    # Wait for the elements to be clickable
    wait = WebDriverWait(driver, 10)

    # # List of texts for the elements you want to click
    # text_list = [
    #     'HSBC Small Cap Fund as on 31 March 2024',
    #     'HSBC Mid Cap Fund as on 31 March 2024',
    #     'HSBC Large Cap Fund as on 31 March 2024',
    #     'HSBC ELSS Tax Saver Fund as on 31 March 2024'
    # ]

    text_list = [
        'HSBC ELSS Tax Saver Fund as on 31 March 2024'
    ]

    # Click on each element one by one
    for text in text_list:
        # Construct XPath to find the element by its text
        xpath = f'//*[contains(text(), "{text}")]'
        print("xpath", xpath)

        # Find the element you want to click
        element = driver.find_element(By.XPATH, xpath)

        # Scroll into view if necessary
        driver.execute_script("arguments[0].scrollIntoView(true);", element)

        # Click on the element
        element.click()
        print("Clicked on the link")

    time.sleep(10)

finally:
    pass
    # Close the WebDriver
    # driver.quit()
    # print("Driver killed")


