import requests
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import csv
import os

def login():
    # Path to your WebDriver executable
    driver_path = 'Your/Driver/Path'

    # Initialize Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("Your/chrome/options")
    chrome_options.add_argument("profile-directory=Default")

    # Initialize the WebDriver
    serv = Service(driver_path)
    driver = webdriver.Chrome(service=serv, options=chrome_options)

    # Open the login page
    driver.get('Your Website')
    # Find the username and password fields and log in

    try:
        username_field = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, 'mat-input-1'))
        )
        # Clear and enter username
        username_field.clear()
        username_field.send_keys(os.getenv('YOUR_EMAIL_ENV_VAR'))

        password_field = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.ID, 'mat-input-0'))
        )
        # Clear and enter password
        password_field.clear()
        password_field.send_keys(os.getenv('YOUR_PASSWORD_ENV_VAR'))

        # Click login button
        login_button = driver.find_element(By.ID, 'submit-button')
        login_button.click()

    except Exception as e:
        print("Already Logged In")
        return driver

    # Wait for the page to load and handle any verification steps
    try:
        # Adjust the waiting time and conditions as per the actual page
        code_field = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.ID, 'code'))
        )

        code = input("Enter 6 Digit code: ")
        if code.lower() == "skip":
            return driver
        code_field.send_keys(code)

        submit_button = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(), 'CONTINUE')]"))
        )
        submit_button.click()

        time.sleep(2)
    except Exception as e:
        print("No verification code input required, continuing...")
        return driver
    return driver

def save_load(driver, rpm, row_element):
    # Get current page handle
    original_handle = driver.current_window_handle

    # Find and click on save icon
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".mat-icon.notranslate.mat-icon-no-color"))
    )
    row_element.find_element(By.CSS_SELECTOR, ".mat-icon.notranslate.mat-icon-no-color").click()

    print("Clicked")
    # Clicking save icon opens a new tab so we must close that tab
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

    new_handle = [handle for handle in driver.window_handles if handle != original_handle][0]
    driver.switch_to.window(new_handle)
    driver.close()

    # Switch back to original tab
    driver.switch_to.window(original_handle)

def open_link(driver, element):
    original_handle = driver.current_window_handle
    found_element = driver.find_element(By.CSS_SELECTOR, element)
    found_element.click()

    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

    new_tab_handle = [handle for handle in driver.window_handles if handle != original_handle][0]
    driver.switch_to.window(new_tab_handle)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.mat-focus-indicator.beta-modal__button.mat-button.mat-button-base.mat-primary')))

    link = driver.current_url

    driver.close()
    driver.switch_to.window(original_handle)

    return found_element, link

def get_loads(driver):
    loads = dict()
    minRPM = 3.30
    maxWeight = 50000

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.row-container.ng-tns-c496-6.ng-star-inserted'))
        )
        row_elements = driver.find_elements(By.CSS_SELECTOR, '.row-container.ng-tns-c496-6.ng-star-inserted')

        for row_element in row_elements:
            this_load = dict()
            try:
                # Get rate per mile
                rate_element = row_element.find_element(By.CSS_SELECTOR, '.calculated-rate.ng-star-inserted')
                rate_text_element = rate_element.find_element(By.TAG_NAME, 'span')
                rate_text = rate_text_element.text.strip()

                # Check for info container, could be different depending on whether the site is fullscreened or not
                try:
                    # Full Screen
                    info_container = row_element.find_element(By.CSS_SELECTOR, '.container-lg.ng-star-inserted')
                    info = info_container.find_elements(By.TAG_NAME, 'span')
                    i = 0
                    for elements in info:
                        if elements.text.strip().endswith(" ft"):
                            this_load["size"] = float(elements.text.strip().replace(" ft", ""))
                            i = 1
                        elif elements.text.strip().endswith(" lbs"):
                            this_load["weight"] = float(elements.text.strip().split(" lbs")[0].replace(",", ""))
                            i = 2
                        else:
                            this_load["type"] = elements.text.strip()

                    if i == 0:
                        raise NoSuchElementException

                except NoSuchElementException:
                    # Not Full Screen
                    try:
                        info_container = row_element.find_element(By.CSS_SELECTOR, '.info-container')
                        info = info_container.find_elements(By.TAG_NAME, 'span')
                        for elements in info:
                            if elements.text.strip().endswith(" ft"):
                                this_load["size"] = float(elements.text.strip().replace(" ft", ""))
                            elif elements.text.strip().endswith(" lbs"):
                                this_load["weight"] = float(elements.text.strip().split(" lbs")[0].replace(",", ""))
                            else:
                                this_load["type"] = elements.text.strip()
                    except NoSuchElementException:
                        pass

                # check for origin and destination info, could be different depending on whether the site is full screen or not
                try:
                    origin_info = row_element.find_element(By.CSS_SELECTOR, '.origin')
                    check = origin_info.find_element(By.CSS_SELECTOR, '.deadhead').text.strip()
                    this_load["origin"] = origin_info.find_element(By.CSS_SELECTOR, '.truncate.extended-trip-point').text.strip()

                    destination_info = row_element.find_element(By.CSS_SELECTOR, '.destination')
                    this_load["destination"] = destination_info.find_element(By.CSS_SELECTOR, '.truncate.extended-trip-point').text.strip()
                except NoSuchElementException:
                    try:
                        origin_info = row_element.find_element(By.CSS_SELECTOR, '.city-state-container')
                        this_load["origin"] = origin_info.find_element(By.CSS_SELECTOR, '.truncate').text.strip() + ", " + origin_info.find_element(By.CSS_SELECTOR, '.state').text.strip()

                        destination_info = row_element.find_element(By.CSS_SELECTOR, '.city-state-container.ng-star-inserted')
                        this_load["destination"] = destination_info.find_element(By.CSS_SELECTOR, '.truncate').text.strip() + ", " + destination_info.find_element(By.CSS_SELECTOR, '.state').text.strip()
                    except NoSuchElementException:
                        pass

                # Should be there every time, but use try block just in case
                try:
                    this_load["pickup"] = row_element.find_element(By.CSS_SELECTOR, '.cell-container.timing-container').text.strip()
                except NoSuchElementException:
                    print("No pickup provided")

                # This will be provided if there is a rpm
                # If this is not provided, skip
                this_load["offer"] = row_element.find_element(By.CSS_SELECTOR, '.offer').text.strip()

                # Check for company
                company = None
                try:
                    company = row_element.find_element(By.CSS_SELECTOR, '.mat-tooltip-trigger.truncate.anchor').text.strip()
                except NoSuchElementException:
                    company = "N/A"

                if rate_text.endswith('*/mi'):
                    # remove non number characters and cast to float
                    rpm = float(rate_text.split('*/mi')[0].replace('$', ''))

                    if rpm >= minRPM and this_load["weight"] <= maxWeight:
                        this_load["rpm"] = rpm
                        save_load(driver, rpm, row_element)
                        loads[company] = this_load

            except NoSuchElementException:
                print("Rate element not found, continuing to next row.")
                continue

            except Exception as e:
                print(f"Error processing rate element: {e}")
                continue

    except Exception as e:
        print(f"Error loading the page: {e}")

    return loads

def send_email(loads, to_email):
    from_email = "YOUR EMAIL"
    from_password = "YOUR PASSWORD"

    to_email = to_email

    subject_base = "Alert"
    body = "\n".join(loads)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(from_email, from_password)

    subject = f"{subject_base} " + ","
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    server.sendmail(from_email, to_email, msg.as_string())

def check_and_notify():
    url = 'YOUR WEBSITE'  # Replace with the actual URL
    min_price = 1000
    max_price = 5000
    min_miles = 100
    max_miles = 1000
    to_email = 'TO EMAIL'

    loads = get_loads(url, min_price, max_price, min_miles, max_miles)
    if loads:
        send_email(loads, to_email)
    else:
        send_email("none", to_email)


driver = login()

driver.get('Your Website')

WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.route-dh-container.lg-flag'))
)
loads = get_loads(driver)
print(loads)
time.sleep(1000)
