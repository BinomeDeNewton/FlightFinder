# Import necessary libraries
from time import sleep, strftime
from random import randint
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox") # mode sans échec
#chrome_options.add_argument("--headless") # sans ouvrir de fenêtre
#chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2, # ne pas charger les images
#})

# Utilisez Service pour spécifier le chemin du chromedriver.
s=Service('/usr/local/bin/chromedriver') # Remplacez chemin_vers_votre_chromedriver par votre chemin réel
driver = webdriver.Chrome(service=s, options=chrome_options)
sleep(2)  

def load_more():
    """Attempts to find and click a 'load more' button, if present."""
    try:
        more_results = '//a[@class = "ULvh"]'  # XPATH to the 'load more' button
        driver.find_elements(By.XPATH, more_results).click()
        print('sleeping.....')
        sleep(randint(25, 35))  # Random sleep to mimic human behavior
    except:
        pass  # If the 'load more' button is not found, do nothing

        
def page_scrape():
    """Scrapes the flight data from the webpage."""
    xp_sections = '//*[@class="xdW8"]'  # XPATH to the sections containing flight info
    sections = driver.find_elements(By.XPATH, xp_sections)
    sections_list = [value.text for value in sections]
    section_a_list = sections_list[::2]  # Splits the list into two for outbound and inbound flights
    section_b_list = sections_list[1::2]

    print(section_a_list)
    print(section_b_list)

    # Handle reCaptcha or empty lists by exiting
    if section_a_list == []:
        raise SystemExit

    # Process outbound and inbound flight info
    a_duration = []
    a_section_names = []
    for n in section_a_list:
        a_section_names.append(''.join(n.split()[2:5]))  # Extracts city names
        a_duration.append(''.join(n.split()[0:2]))  # Extracts flight duration
    b_duration = []
    b_section_names = []
    for n in section_b_list:
        b_section_names.append(''.join(n.split()[2:5]))
        b_duration.append(''.join(n.split()[0:2]))

    # Extract dates
    xp_dates = '//div[@class="c9L-i"]'
    dates = driver.find_elements(By.XPATH, xp_dates)
    dates_list = [value.text for value in dates]
    a_date_list = dates_list[::2]
    b_date_list = dates_list[1::2]
    a_day = [value.split()[0] for value in a_date_list]  # Separates the day
    a_weekday = [value.split()[1] for value in a_date_list]  # Separates the weekday
    b_day = [value.split()[0] for value in b_date_list]
    b_weekday = [value.split()[1] for value in b_date_list]

    # Extract prices
    xp_prices = '//div[@class="oVHK"]'
    prices = driver.find_elements(By.XPATH, xp_prices)
    prices_list = [price.text.replace('$', '') for price in prices if price.text != '']
    filtered_prices_list = [p for p in prices_list if p.replace(',', '').isdigit()]
    prices_list_int = [int(price.replace(',', '')) for price in filtered_prices_list]

    # Extract stopover information
    xp_stops = '//div[@class="JWEO"]/div[1]'
    stops = driver.find_elements(By.XPATH, xp_stops)
    stops_list = [stop.text[0].replace('n', '0') for stop in stops]  # Replaces 'n' with '0' for non-stop flights
    a_stop_list = stops_list[::2]
    b_stop_list = stops_list[1::2]

    xp_stops_cities = '//div[@class="JWEO"]/div[2]'
    stops_cities = driver.find_elements(By.XPATH, xp_stops_cities)
    stops_cities_list = [stop.text for stop in stops_cities]
    a_stop_name_list = stops_cities_list[::2]
    b_stop_name_list = stops_cities_list[1::2]

    # Extract airline, departure, and arrival times for both legs
    xp_schedule = '//div[@class="VY2U"]'
    schedules = driver.find_elements(By.XPATH, xp_schedule)
    hours_list = []
    carrier_list = []
    for schedule in schedules:
        hours_list.append(schedule.text.split('\n')[0])  # Splits and extracts hours
        carrier_list.append(schedule.text.split('\n')[1])  # Splits and extracts carrier name
    a_hours = hours_list[::2]
    a_carrier = carrier_list[::2]
    b_hours = hours_list[1::2]
    b_carrier = carrier_list[1::2]

    # Define the columns for the DataFrame
    cols = (['Out Day', 'Out Time', 'Out Weekday', 'Out Airline', 'Out Cities', 'Out Duration', 'Out Stops', 'Out Stop Cities',
             'Return Day', 'Return Time', 'Return Weekday', 'Return Airline', 'Return Cities', 'Return Duration', 'Return Stops', 'Return Stop Cities',
             'Price'])
    
    # Create the DataFrame
    flights_df = pd.DataFrame({'Out Day': a_day,
                               'Out Weekday': a_weekday,
                               'Out Duration': a_duration,
                               'Out Cities': a_section_names,
                               'Return Day': b_day,
                               'Return Weekday': b_weekday,
                               'Return Duration': b_duration,
                               'Return Cities': b_section_names,
                               'Out Stops': a_stop_list,
                               'Out Stop Cities': a_stop_name_list,
                               'Return Stops': b_stop_list,
                               'Return Stop Cities': b_stop_name_list,
                               'Out Time': a_hours,
                               'Out Airline': a_carrier,
                               'Return Time': b_hours,
                               'Return Airline': b_carrier,
                               'Price': prices_list_int})[cols]
    
    flights_df['timestamp'] = strftime("%Y%m%d-%H%M")  # Adds a timestamp for when the scrape occurred
    return flights_df
def start_kayak(city_from, city_to, date_start, date_end):
    """This function starts a search on Kayak for flights.
    
    Parameters:
    city_from (str): IATA code of the departure city.
    city_to (str): IATA code of the arrival city.
    date_start (str): Start date of the journey in YYYY-MM-DD format.
    date_end (str): End date of the journey in YYYY-MM-DD format.
    """
    
    # Construct the URL for the Kayak search
    kayak = ('https://www.kayak.com/flights/' + city_from + '-' + city_to +
             '/' + date_start + '-flexible/' + date_end + '-flexible?sort=bestflight_a')
    driver.get(kayak)  # Open the Kayak search URL with Selenium
    sleep(randint(8,10))  # Random sleep to mimic human behavior
    
    # Attempt to close any pop-up that appears
    try:
        xp_popup_close = '//button[contains(@id,"dialog-close") and contains(@class,"Button-No-Standard-Style close ")]'
        driver.find_elements(By.XPATH, xp_popup_close)[5].click()  # Try to find and click the close button
    except Exception as e:
        pass  # If no pop-up is found or any error occurs, just pass
    sleep(randint(60,95))  # Random sleep to mimic human behavior

    print('loading more.....')    
    load_more()  # Call the function to load more results if available
    
    print('starting first scrape.....')
    df_flights_best = page_scrape()  # Scrape the page for the best flights
    df_flights_best['sort'] = 'best'  # Add a column indicating these are the 'best' sorted results
    sleep(randint(60,80))  # Random sleep to mimic human behavior
    
    # Now, let's handle the lowest prices from the price matrix at the top of the page
    matrix = driver.find_elements(By.XPATH, '//*[contains(@id,"FlexMatrixCell")]')  # Find all elements in the price matrix
    matrix_prices = [price.text.replace('$', '') for price in matrix if price.text.startswith('$')]  # Extract prices
    # Filter to ensure only items with a price are converted
    filtered_matrix_prices = [p for p in matrix_prices if p.replace(',', '').isdigit()]
    # Convert filtered prices to integers after removing commas
    matrix_prices_int = [int(p.replace(',', '')) for p in filtered_matrix_prices]
    matrix_min = min(matrix_prices_int)  # Find the minimum price
    matrix_avg = sum(matrix_prices_int) / len(matrix_prices_int)  # Calculate the average price
    
    print('switching to cheapest results.....')
    # XPath to find and click the button to sort by cheapest flights
    cheap_results_xpath = "//div[contains(@class, 'Hv20-option') and @aria-label='Cheapest']"
    try:
        driver.find_element(By.XPATH, cheap_results_xpath).click()  # Try to click the cheapest sort option
    except Exception as e:
        print("Exception when clicking for more results:", e)
    
    sleep(randint(60,90))  # Random sleep to mimic human behavior
    
    print('loading more.....')
    load_more()  # Load more results if available
    
    print('starting second scrape.....')
    df_flights_cheap = page_scrape()  # Scrape the page for the cheapest flights
    df_flights_cheap['sort'] = 'cheap'  # Add a column indicating these are the 'cheap' sorted results
    sleep(randint(60,80))  # Random sleep to mimic human behavior
    
    print('switching to quickest results.....')
    # XPath to find and click the button to sort by quickest flights
    quick_results_xpath = "//div[contains(@class, 'Hv20-option') and @aria-label='Quickest']"
    driver.find_element(By.XPATH, quick_results_xpath).click()  # Click the quickest sort option
    sleep(randint(60,90))  # Random sleep to mimic human behavior
    print('loading more.....')
    
    load_more()  # Load more results if available
    
    print('starting third scrape.....')
    df_flights_fast = page_scrape() # Scrape the page for the quickest flights
    df_flights_fast['sort'] = 'quick' # Add a column indicating these are the 'quick' sorted results
    sleep(randint(60,80)) # Random sleep to mimic human behavior
    
    # Concatenate the dataframes from the three different sorts into one
    final_df = pd.concat([df_flights_cheap, df_flights_best, df_flights_fast])
    # Path where you want to save the Excel file
    backup_folder = 'search_backups'
    # Make sure that the folder path exists, otherwise create it
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        
    # Build the complete path of the file
    file_name = '{}_flights_{}-{}_from_{}_to_{}.xlsx'.format(strftime("%Y%m%d-%H%M"), city_from, city_to, date_start, date_end)
    full_path = os.path.join(backup_folder, file_name)
    
    # Save the DataFrame in an Excel file
    final_df.to_excel(full_path, index=False)
    print('saved df.....')

    driver.save_screenshot('pythonscraping.png')
    driver.quit()

def main() :
    # Définition des paramètres pour la recherche de vol
    city_from = "CDG"  # Code IATA pour l'aéroport de départ, exemple : CDG pour Paris Charles de Gaulle
    city_to = "JFK"  # Code IATA pour l'aéroport d'arrivée, exemple : JFK pour New York John F. Kennedy
    date_start = "2024-05-01"  # Date de départ souhaitée au format AAAA-MM-JJ
    date_end = "2024-05-10"  # Date de retour souhaitée au format AAAA-MM-JJ
    
    # Appel de la fonction pour démarrer la recherche de vol sur Kayak
    start_kayak(city_from, city_to, date_start, date_end)
    
if __name__ == "__main__":
    main()
    