# FlightFinder

**FlightFinder** is a Python script designed to automate the search and analysis of flight information by web scraping on sites like Kayak. This script allows users to retrieve data on flights, including prices, schedules, and durations, and then save it for later analysis.

## Table of Contents

- [Prerequisites](#prerequisites)
  - [Installing Dependencies](#installing-dependencies)
  - [Configuring ChromeDriver](#configuring-chromedriver)
- [Usage](#usage)
- [Analyzing the Results](#analyzing-the-results)
- [Compatibility](#compatibility)

## Prerequisites

### Installing Dependencies

Before launching **FlightFinder**, make sure you have installed Python 3 and the necessary packages. You can install all required packages using the pip package manager. Open a terminal and execute the following command:

```sh
pip install selenium pandas
```

### Configuring ChromeDriver

**FlightFinder** uses Selenium with ChromeDriver to automate browser interactions. Follow these steps to set up ChromeDriver on your system:

1. **Download ChromeDriver**: Go to [the ChromeDriver download page](https://sites.google.com/chromium.org/driver/) and download the version that matches your Google Chrome version.

2. **Installation**:
   - **Windows**: Unzip the downloaded file and move `chromedriver.exe` to a folder of your choice. Add the folder path to the `PATH` environment variable.
   - **MacOS/Linux**: Unzip the downloaded file and move `chromedriver` to `/usr/local/bin` or another folder included in your `PATH`.

3. **Updating**: Make sure to regularly check for updates to ChromeDriver to keep it compatible with your Chrome browser.

## Usage

To use **FlightFinder**, follow these steps:

1. **Configure search settings**: Modify the `city_from`, `city_to`, `date_start`, and `date_end` variables in the script to match your flight search criteria.

2. **Launch the Script**: Run the script in your terminal or command prompt:

```sh
python flightfinder.py
```

## Analyzing the Results

After running the script, the scraping results will be saved in an Excel file in the `search_backups` folder. Each file contains detailed information on the found flights, including prices, schedules, durations, and more.

- **Open the Excel file**: Use your favorite spreadsheet software to open the file.
- **Analyze the data**: You can sort, filter, and perform statistical analyses on the data to find the best flight deals according to your criteria.

## Compatibility

**FlightFinder** has been tested and is compatible with recent versions of Python (3.6+) and Selenium. Make sure your Google Chrome browser is also up-to-date to avoid any compatibility issues with ChromeDriver.

---

⚠️ Remember to update the path to ChromeDriver in the script (`s=Service('/usr/local/bin/chromedriver')`) according to where you've moved it on your system.
