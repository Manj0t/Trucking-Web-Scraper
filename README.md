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
