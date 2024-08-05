import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import os
import sys
import pygame
import time
import math

load_counter = 0
def enter_verification_code():
    """
    Opens a Pygame window for the user to enter a verification code.
    The code is limited to 6 digits and can be submitted by pressing Enter.

    Returns:
        text (str): The entered verification code.
    """
    pygame.init()

    # Set up the window
    screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption('Enter Verification Code')

    # Define fonts
    input_box = pygame.Rect(100, 100, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        # Utilizes variable text size depending on whether or not the user has inputted anything
        size = 50 if text else 25
        font = pygame.font.Font(None, size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            # Handles logic for typing
            if event.type == pygame.KEYDOWN:
                if active:
                    # Checks if enter button has been clicked to submit code
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 6:  # Limit input to 6 digits
                            text += event.unicode

        screen.fill((30, 30, 30))
        placeholder = "Enter Verification Code"
        txt_surface = font.render(text, True, color) if text else font.render(placeholder, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    pygame.quit()
    return text

"""
Logs into a specified website using credentials stored in environment variables.
Handles potential verification steps requiring user input via a Pygame window.

Returns:
     driver (webdriver.Chrome): The WebDriver instance after logging in.
"""
def login():
    # Path to your WebDriver executable
    driver_path = 'Path/To/Your/Driver' # Element Needs to Be Changed

    # Initialize Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-data-dir=Path/To/Your/Chrome/File") # Element Needs to Be Changed
    chrome_options.add_argument("profile-directory=Default")

    # Initialize the WebDriver
    serv = Service(driver_path)
    driver = webdriver.Chrome(service=serv, options=chrome_options)

    # Open the login page
    driver.get('YOUR WEBSITE') # Element Needs to Be Changed
    # Find the username and password fields and log in

    try:
        username_field = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, 'mat-input-1'))
        )
        # Clear and enter username
        username_field.clear()
        username_field.send_keys(os.getenv('YOUR_EMAIL_ENV_VAR')) # Element Needs to Be Changed

        password_field = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.ID, 'mat-input-0'))
        )
        # Clear and enter password
        password_field.clear()
        password_field.send_keys(os.getenv('YOUR_PASSWORD_ENV_VAR')) # Element Needs to Be Changed

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

        code = enter_verification_code()

        # Skip case incase user manually inputs code
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

"""
Inputs the start and end dates in their respective fields on the webpage.

Args:
    driver (webdriver.Chrome): The WebDriver instance to interact with.
    end_date (str): The end date to input.
    start_date (str): The start date to input.
"""
def input_date(driver, end_date, start_date):
    # Checks if neither dates were given
    if start_date == end_date == '':
        return
    # Wait for the start date input field to be present
    start_date_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[matstartdate]'))
    )

    # Wait for the end date input field to be present
    end_date_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[matenddate]'))
    )

    # Clear the input fields and send keys
    if start_date != '':
        start_date_field.send_keys('\ue003' * 10)
        start_date_field.send_keys(start_date)
    if end_date != '':
        end_date_field.send_keys('\ue003' * 10)
        end_date_field.send_keys(end_date)

"""
Searches for the origin location by inputting it in the specified field.

Args:
    driver (webdriver.Chrome): The WebDriver instance to interact with.
    origin (str): The origin location to search for.
"""
def search_origin(driver, origin):
    try:
        origin_field = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.ID, 'mat-input-2'))
        )

        origin_field.clear()

        origin_field.send_keys(origin)

        time.sleep(1)

        options = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.mat-autocomplete-panel.locations-panel.ng-star-inserted.mat-autocomplete-visible'))
        )
        best_option = WebDriverWait(options, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mat-option-text"))
        )
        best_option.click()
    except Exception as e:
        pass

"""
Searches for the destination location by inputting it in the specified field.

Args:
    driver (webdriver.Chrome): The WebDriver instance to interact with.
    destination (str): The destination location to search for.
"""
def search_destination(driver, destination):
    destination_field = WebDriverWait(driver, 6).until(
        EC.presence_of_element_located((By.ID, 'mat-input-3'))
    )
    destination_field.clear()
    time.sleep(1)
    destination_field.send_keys(destination)
    time.sleep(1)

"""
Saves a load by clicking on the save icon and handling the newly opened tab.

Args:
    driver (webdriver.Chrome): The WebDriver instance to interact with.
    row_element (WebElement): The row element containing the load details.
"""
def save_load(driver, row_element):
    # Get current page handle
    original_handle = driver.current_window_handle

    # Find and click on save icon
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".mat-icon.notranslate.mat-icon-no-color"))
    )
    row_element.find_element(By.CSS_SELECTOR, ".mat-icon.notranslate.mat-icon-no-color").click()

    # Clicking save icon opens a new tab so we must close that tab
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

    new_handle = [handle for handle in driver.window_handles if handle != original_handle][0]
    driver.switch_to.window(new_handle)
    driver.close()

    # Switch back to original tab
    driver.switch_to.window(original_handle)

"""
Retrieves loads from the webpage that meet the specified criteria.

Args:
    show_similar_results (bool): Whether or not to show similar results.
    driver (webdriver.Chrome): The WebDriver instance to interact with.
    minRPM (float): The minimum rate per mile for the loads.
    maxWeight (float): The maximum weight for the loads.

Returns:
    loads (dict): A dictionary of loads that meet the criteria.
"""
def get_loads(show_similar_results, driver, maxWeight, minOffer, minRPM):
    loads = dict()
    global load_counter

    try:
        # Check if similar results should be on or off, by default it is on
        if not show_similar_results:
            try:
                similar_result_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.mat-slide-toggle-thumb'))
                )
                similar_result_button.click()
            except:
                pass
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.row-container.ng-tns-c497-6.ng-star-inserted'))
        )
        row_elements = driver.find_elements(By.CSS_SELECTOR, '.row-container.ng-tns-c497-6.ng-star-inserted')
        for row_element in row_elements:
            this_load = dict()
            try:
                # Get rate per mile
                rate_element = row_element.find_element(By.CSS_SELECTOR, '.calculated-rate.ng-star-inserted')
                if minRPM < math.inf:
                    try:
                        rate_text = rate_element.find_element(By.TAG_NAME, 'span').text.strip()
                    except Exception as e:
                        rate_text = '$' + str(-math.inf) + '*/mi'
                else:
                    rate_text = '$' + str(-math.inf) + '*/mi'
                if minOffer < math.inf:
                    try:
                        offer_element = row_element.find_element(By.CSS_SELECTOR, '.offer').text.strip()
                    except Exception as e:
                        offer_element = '$' + str(-math.inf)
                else:
                    offer_element = '$' + str(-math.inf)

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
                    # i will be 0 if the if statments don't hit, i.e. it's not full screen
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

                    # check will only be possible depending on the screen size, if check doesn't work an exception will be thrown and the other try block will run
                    check = origin_info.find_element(By.CSS_SELECTOR, '.route-icon.ng-star-inserted')
                    this_load["origin"] = origin_info.find_element(By.CSS_SELECTOR, '.truncate.extended-trip-point').text.strip()

                    destination_info = row_element.find_element(By.CSS_SELECTOR, '.destination')
                    this_load["destination"] = destination_info.find_element(By.CSS_SELECTOR, '.truncate.extended-trip-point').text.strip()
                except NoSuchElementException:
                    try:
                        origin_info = row_element.find_element(By.CSS_SELECTOR, '.city-state-container')
                        this_load["origin"] = origin_info.find_element(By.CSS_SELECTOR, '.truncate').text.strip() + ", " + origin_info.find_element(By.CSS_SELECTOR, '.state').text.strip()

                        destination_info = row_element.find_element(By.CSS_SELECTOR, '.city-state-container.ng-star-inserted')
                        this_load["destination"] = destination_info.find_element(By.CSS_SELECTOR, '.truncate').text.strip() + ", " + destination_info.find_element(
                            By.CSS_SELECTOR, '.state').text.strip()
                    except NoSuchElementException:
                        pass

                # Should be there every time, but use try block just in case
                try:
                    this_load["pickup"] = row_element.find_element(By.CSS_SELECTOR, '.cell-container.timing-container').text.strip()
                except NoSuchElementException:
                    print("No pickup provided")

                # Check for company
                try:
                    this_load["company"] = row_element.find_element(By.CSS_SELECTOR, '.mat-tooltip-trigger.truncate.anchor').text.strip()
                except NoSuchElementException:
                    this_load["company"] = "N/A"

                if rate_text.endswith('*/mi'):
                    # remove non number characters and cast to float
                    rpm = float(rate_text.split('*/mi')[0].replace('$', ''))
                    offer = offer_element.replace('$', '')
                    if offer.find(',') != -1:
                        offer = float(offer.replace(',', ''))
                    else:
                        offer = float(offer)
                    print(offer)
                    if rpm >= minRPM and this_load["weight"] <= maxWeight or offer >= minOffer and this_load["weight"] <= maxWeight:
                        this_load["rpm"] = rpm
                        this_load["offer"] = offer
                        save_load(driver, row_element)
                        loads[f"load_{load_counter}"] = this_load
                        load_counter += 1

            except NoSuchElementException:
                continue

            except Exception as e:
                print(f"Error processing rate element: {e}")
                continue

    except Exception as e:
        print(f"Error loading the page: {e}")

    return loads


"""
Sends an email with the details of loads that meet specified criteria.

Args:
    loads (dict): A dictionary of loads with their details.
    to_email (str): The recipient email address.
"""
def send_email(loads, to_email):
    from_email = "YOUR FROM EMAIL" # Element Needs to Be Changed
    from_password = "APP PASSWORD" # Element Needs to Be Changed

    subject = "ALERT"
    body = ""

    # Uses html to format email
    for key, load in loads.items():
        company = load['company']
        origin = load['origin']
        destination = load['destination']
        offer = load['offer']
        rpm = load['rpm']
        pickup = load['pickup']
        weight = load['weight']
        size = load['size']
        type_ = load['type']

        body += f"""
            <h1>{company}</h1>
            <h2>{origin} - {destination}</h2>
            <p>Offer: {offer}</p>
            <p>Rate: {rpm}</p>
            <p>Pickup: {pickup}</p>
            <p>Weight: {weight}</p>
            <p>Size: {size}</p>
            <p>Type: {type_}</p>
            <br>
            """

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(from_email, from_password)

    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    server.sendmail(from_email, to_email, msg.as_string())

"""
Executes the entire job sequence of logging in, searching for loads, and sending email alerts.

Args:
    show_similar_results (bool): Whether or not to show similar results.
    minRPM (float): The minimum rate per mile for the loads.
    maxWeight (float): The maximum weight for the loads.
    origin (str): The origin location for the search.
    end_date (str): The end date for the search.
    start_date (str): The start date for the search.
    locations (list): A list of destination locations to search for.
"""
def job(show_similar_result, minRPM, minOffer, maxWeight, origin, end_date, start_date, locations):
    loads = dict()
    driver = login()

    driver.get('YOUR WEBSITE') # Element Needs to Be Changed

    input_date(driver, end_date, start_date)

    for location in locations:
        if location == '':
            continue
        search_destination(driver, location)

        # Causes issues if origin is not searched every loop
        search_origin(driver, origin)

        search_icon = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.ID, "search-automation"))
        )
        search_icon.click()

        # Give time for page to load before moving on
        time.sleep(2)

        these_loads = get_loads(show_similar_result, driver, maxWeight, minOffer, minRPM)

        for key in these_loads:
            if these_loads[key] not in loads.values():
                loads[key] = these_loads[key]

    if loads:
        to_email = "YOUR TO EMAIL" # Element Needs to Be Changed
        send_email(loads, to_email)

    driver.quit()