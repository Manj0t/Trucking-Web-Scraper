import requests
from bs4 import BeautifulSoup
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
import os

def login():
    # Path to your WebDriver executable
    driver_path = 'Your/Path/To/your/chromedriver'

    # Initialize Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("Path/To/ChromeOptions")
    chrome_options.add_argument("profile-directory=Default")

    # Initialize the WebDriver
    serv = Service(driver_path)
    driver = webdriver.Chrome(service=serv, options=chrome_options)

    # Open the login page
    driver.get('Webpage')
    # Find the username and password fields and log in

    try:
        username_field = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, 'mat-input-1'))
        )
        # Clear and enter username
        #Using environmental variabls for security
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

def scroll_to_element(driver, scrollable_selector, target_element):
    try:
        scrollable_element = driver.find_element(By.CSS_SELECTOR, scrollable_selector)
        target = scrollable_element.find_element(By.CSS_SELECTOR, target_element)

        driver.execute_script("arguments[0].scrollTop = arguments[1].offsetTop;", scrollable_element, target)
        time.sleep(2)
    except NoSuchElementException:
        print(f"Element not found: {target_element}")
    except Exception as e:
        print(f"Error scrolling to element: {e}")
def click_element_using_js(row_element, element_selector, driver):
    try:
        element = row_element.find_element(By.CSS_SELECTOR, element_selector)

        # Use JavaScript to click the element
        driver.execute_script("arguments[0].click();", element)

    except NoSuchElementException:
        print(f"Element not found: {element_selector}")
    except Exception as e:
        print(f"Error clicking the element: {e}")


def save_load(driver, rpm, row_element):
    directory = 'Your/Directory/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    element = '.route-dh-container.lg-flag'
    scroller_element = ".cdk-virtual-scroll-viewport"
    scroll_to_element(driver, scroller_element, row_element)
    click_element_using_js(row_element, element, driver)

    time.sleep(2)

    filename = f'load_{time.time()}_{rpm}.png'
    filepath = os.path.join(directory, filename)
    driver.save_screenshot(filepath)


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

    # Example parsing logic (you need to adjust according to the webpage structure)
    loads = dict()
    minRPM = 2.50

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.row-container.ng-tns-c496-6.ng-star-inserted'))
        )
        row_elements = driver.find_elements(By.CSS_SELECTOR, '.row-container.ng-tns-c496-6.ng-star-inserted')

        for row_element in row_elements:
            try:
                rate_element = row_element.find_element(By.CSS_SELECTOR, '.calculated-rate.ng-star-inserted')
                rate_text_element = rate_element.find_element(By.TAG_NAME, 'span')
                rate_text = rate_text_element.text.strip()

                if rate_text.endswith('*/mi'):
                    rpm = float(rate_text.split('*/mi')[0].replace('$', ''))

                    if rpm >= minRPM:
                        save_load(driver, rpm, row_element)
                        loads[rpm] = rpm

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
    from_email = "YourEmail"
    from_password = "Your Password"

    to_email = to_email

    subject_base = "Alert"
    body = "\n".join(loads)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(from_email, from_password)

    subject = f"{subject_base} " + "," * i
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    server.sendmail(from_email, to_email, msg.as_string())

def check_and_notify():
    url = 'Webpage'  # Replace with the actual URL
    min_price = 1000
    max_price = 5000
    min_miles = 100
    max_miles = 1000
    to_email = 'ToEmail'

    loads = get_loads(url, min_price, max_price, min_miles, max_miles)
    if loads:
        send_email(loads, to_email)
    else:
        send_email("none", to_email)

# Schedule the job to run every hour
# schedule.every().hour.do(check_and_notify)

driver = login()

driver.get('Webpage')

WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.route-dh-container.lg-flag'))
    )
loads = get_loads(driver)
print(loads)
time.sleep(1000)
