import json
import csv
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta


# Function to scrape currency rates from the source website
def scrape_currency_rates():
    url = 'https://do.scotiabank.com/banca-personal/tarifas/tasas-de-cambio.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    currency_data = {}

    table = soup.find('table', {'class': 'bns--table'})
    rows = table.find_all('tr')

    for row in rows[1:]:
        columns = row.find_all('td')

        if len(columns) >= 4:
            currency_info = columns[1].text.strip()
            currency_code = currency_info.split('(')[-1].split(')')[0]
            compra = float(columns[2].text.strip())
            venta = float(columns[3].text.strip())

            currency_data[currency_code] = {'compra': compra, 'venta': venta}

    return currency_data


# Read the JSON file
with open('tasas.json') as json_file:
    data = json.load(json_file)

# Get yesterday's date
yesterday = str(date.today() - timedelta(days=1))

# Extract previous day's data and save it to a CSV file
previous_day_data = data.get(yesterday)
if previous_day_data:
    filename = 'previous_day_data.csv'
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Date', 'Currency', 'Compra', 'Venta'])
        for currency, values in previous_day_data['currencies'].items():
            compra = values['compra']
            venta = values['venta']
            writer.writerow([yesterday, currency, compra, venta])
    print(f"Previous day's data saved to {filename}")

# Get today's date
today = str(date.today())

# Scrape currency rates data
today_data = scrape_currency_rates()

# Update the dictionary with today's data
data[today] = {'currencies': today_data}

# Write the updated dictionary back to the JSON file
with open('tasas.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"Data for {today} updated in data.json")

