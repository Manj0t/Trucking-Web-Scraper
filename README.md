# Load Information Scraper

## Overview

This project is designed to scrape load information from a website based on user-defined criteria, such as minimum rate per mile and maximum weight. The project consists of two main components:

**runner.py**: A Pygame-based graphical user interface (GUI) that allows users to input criteria for the scraping process and control the execution of the scraping program.

**scrapingLogic.py**: Contains the scraping logic implemented using Selenium WebDriver, handles user login, input of dates and locations, and retrieves load information.

## Requirements

- Python **3.10.12**
- **Pygame**
- **Selenium**
- **ChromeDriver**

## Installation

1. **Clone the repository**.
2. **Install the required Python packages using pip**:
    ```bash
    pip install pygame selenium
    ```
3. **Ensure you have ChromeDriver installed and available in your PATH or specify its path in scrapingLogic.py**.

## Usage

### runner.py

This script provides a GUI for users to input criteria for the scraping process and start/stop the scraping program.

**Running the Script:**

```bash
python runner.py

**GUI Components:**

- **TextInput**: Input boxes for entering the minimum rate, maximum weight, origin, start date, end date, and destination.
- **Buttons**:
  - **Start**: Begins the scraping process.
  - **Stop Program**: Stops the scraping process if it is running.
  - **Add More Destination Input Boxes**: Adds more input boxes for entering additional destinations.
  - **Remove Input**: Removes the last input box.

**scrapingLogic.py**

This script contains the logic for logging into the website, handling potential verification steps, and retrieving load information based on the criteria entered in the GUI.

**Functions:**

- **enter_verification_code()**: Opens a Pygame window for the user to enter a verification code.
- **login()**: Logs into the website using credentials stored in environment variables.
- **input_date()**: Inputs the start and end dates on the webpage.
- **search_origin()**: Searches for the origin location on the webpage.
- **search_destination()**: Searches for the destination location on the webpage.
- **save_load()**: Saves a load by clicking on the save icon.
- **get_loads()**: Retrieves loads that meet the specified criteria.

**Configuration**

**Environment Variables**

Store your login credentials in environment variables:

- **YOUR_EMAIL_ENV_VAR**: Your email used for login.
- **YOUR_PASSWORD_ENV_VAR**: Your password used for login.

**ChromeDriver Path**

Specify the path to your ChromeDriver executable in scrapingLogic.py:

```python
driver_path = 'Path/To/Your/Driver'
