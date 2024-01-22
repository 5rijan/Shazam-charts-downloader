import requests
import time
import os
from datetime import datetime
import logging


def countries():
    return ['world','algeria','argentina','argentina/buenos-aires', 'australia','australia/adelaide','australia/brisbane','australia/melbourne','australia/perth','australia/sydney',
             'austria','azerbaijan', 'belarus', 'belgium', 'brazil','brazil/brasília','brazil/rio-de-janeiro','brazil/s%C3%A3o-paulo', 'bulgaria','cameroon', 'canada', 'canada/calgary',
             'canada/edmonton','canada/london','canada/montr%C3%A9al','canada/ottawa','canada/qu%C3%A9bec','canada/toronto','canada/vancouver','chile','chile/santiago', 'china','china/beijing',
             'china/shanghai', 'colombia','colombia/bogot%C3%A1','colombia/medell%C3%ADn', 'costa-rica', 'croatia', 'czechia','ivory-coast', 'denmark', 'denmark/copenhagen', 'egypt',
             'finland','finland/helsinki', 'france','france/bordeaux','france/le-havre','france/lyon','france/marseille','france/montpellier','france/nantes','france/nice','france/paris'
             ,'france/strasbourg','france/toulouse', 'germany','germany/berlin', 'germany/d%C3%BCsseldorf','germany/essen','germany/frankfurt-am-main','germany/hamburg','germany/hannover','germany/k%C3%B6ln',
             'germany/mannheim','germany/munich','germany/stuttgart',  'ghana', 'greece','greece/athens', 'hungary', 'india', 'india/bengaluru','india/delhi','india/mumbai', 'indonesia',
             'ireland','ireland/dublin', 'israel','israel/tel-aviv', 'italy','italy/florence','italy/milan','italy/naples','italy/palermo','italy/rome','italy/turin','italy/venice', 'japan',
             'japan/osaka','japan/tokyo', 'kazakhstan','kenya', 'malaysia', 'mexico','mexico/guadalajara', 'mexico/mexico-city','mexico/monterrey','mexico/puebla', 'mexico/tijuana', 'mexico/toluca',
             'mozambique', 'morocco', 'netherlands','netherlands/amsterdam','netherlands/maastricht', 'netherlands/rotterdam', 'netherlands/the-hague', 'netherlands/utrecht', 'new-zealand',
             'nigeria','nigeria/benin-city', 'nigeria/kaduna', 'nigeria/kano', 'nigeria/lagos', 'nigeria/port-harcourt', 'norway', 'norway/oslo', 'peru', 'peru/lima', 'philippines','poland',
             'poland/kraków', 'poland/warsaw', 'portugal', 'portugal/lisbon','portugal/porto', 'romania', 'romania/bucharest', 'russia', 'russia/moscow', 'russia/saint-petersburg', 'saudi-arabia',
             'singapore', 'singapore/singapore', 'senegal', 'south-africa','south-africa/cape-town', 'south-africa/durban', 'south-africa/johannesburg', 'south-korea', 'south-korea/seoul',
             'spain', 'spain/barcelona', 'spain/madrid', 'spain/sevilla', 'spain/valencia', 'sweden', 'sweden/göteborg', 'sweden/malmö', 'sweden/stockholm', 'switzerland','tanzania',
             'thailand','thailand/bangkok', 'tunisia', 't%C3%BCrkiye', 't%C3%BCrkiye/adana', 't%C3%BCrkiye/ankara','t%C3%BCrkiye/istanbul', 'ukraine','ukraine/kyiv', 'united-arab-emirates',
             'united-arab-emirates/dubai', 'united-kingdom', 'united-kingdom/belfast', 'united-kingdom/birmingham', 'united-kingdom/bristol', 'united-kingdom/brighton', 'united-kingdom/cardiff',
             'united-kingdom/edinburgh', 'united-kingdom/glasgow', 'united-kingdom/leeds', 'united-kingdom/liverpool', 'united-kingdom/london', 'united-kingdom/manchester', 'united-kingdom/newcastle-upon-tyne',
             'united-kingdom/nottingham', 'united-kingdom/portsmouth', 'united-kingdom/sheffield', 'united-states', 'united-states/albany', 'united-states/atlanta', 'united-states/baltimore', 'united-states/boston',
             'united-states/buffalo', 'united-states/charlotte', 'united-states/chicago', 'united-states/cincinnati', 'united-states/cleveland','united-states/columbia', 'united-states/columbus',
             'united-states/corpus-christi', 'united-states/dallas', 'united-states/denver', 'united-states/detroit', 'united-states/el-paso', 'united-states/fresno', 'united-states/honolulu', 'united-states/houston',
             'united-states/indianapolis', 'united-states/irvine', 'united-states/jacksonville', 'united-states/kansas-city', 'united-states/las-vegas', 'united-states/long-island', 'united-states/los-angeles',
             'united-states/louisville', 'united-states/memphis', 'united-states/miami', 'united-states/minneapolis', 'united-states/nashville', 'united-states/new-haven',  'united-states/new-orleans', 'united-states/new-york-city',
             'united-states/newark', 'united-states/oklahoma-city', 'united-states/orlando', 'united-states/philadelphia', 'united-states/phoenix', 'united-states/pittsburgh', 'united-states/portland-or', 'united-states/raleigh',
             'united-states/sacramento', 'united-states/salt-lake-city', 'united-states/san-antonio', 'united-states/san-bernardino', 'united-states/san-diego', 'united-states/san-francisco', 'united-states/seattle',
             'united-states/st.-louis', 'united-states/tampa', 'united-states/virginia-beach', 'united-states/washington-d.c.', 'united-states/yonkers',
             'uruguay','uzbekistan','uzbekistan/tashkent', 'venezuela','vietnam','zambia']


logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def download_country(country, today, i, total_countries):
    print(f"Downloading file for {country} ({i}/{total_countries}, {i/total_countries*100:.2f}%)")

    # Split the country variable into country_name and city_name
    parts = country.split('/')
    country_name = parts[0]
    city_name = parts[1] if len(parts) > 1 else ''

    # Check if the country string contains a '/'
    if city_name:
        url = f'https://www.shazam.com/services/charts/csv/top-50/{country}/'
    else:
        url = f'https://www.shazam.com/services/charts/csv/top-200/{country_name}/'
    
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as err:
        logging.error(f"Error occurred while downloading file for {country}: {err}")
        return

    # Create the necessary subdirectories
    os.makedirs(os.path.join(today, country_name, city_name), exist_ok=True)
    filename = f'{country_name}-{city_name}-{today}.csv' if city_name else f'{country_name}-{today}.csv'
    with open(os.path.join(today, country_name, city_name, filename), 'wb') as file:
        for data in response.iter_content(1024):
            file.write(data)
    time.sleep(1)
    

def main():
    # Get today's date and format it as DD-MM-YYYY
    today = datetime.now().strftime('%d-%m-%Y')

    # Create a new directory with today's date
    os.makedirs(today, exist_ok=True)

    action = input("Do you want to (1) download the whole database, (2) update the whole database, or (3) download a specific country? Enter the number: ")

    if action == "1" or action == "2":
        country_list = countries()
        total_countries = len(country_list)
        for i, country in enumerate(country_list, start=1):
            download_country(country, today, i, total_countries)
    elif action == "3":
        country = input("Enter the country (and optionally city) in the format 'country/city': ")
        download_country(country, today, 1, 1)
    else:
        print("Invalid input. Please run the script again.")

if __name__ == "__main__":
    main()


