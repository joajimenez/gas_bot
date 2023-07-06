import json
import datetime

def calculate_percentage_change(today, yesterday):
    return ((today - yesterday) / yesterday) * 100

def print_percentage_change(percentage_change):
    if percentage_change > 0:
        print(f"+{percentage_change:.2f}%")
    elif percentage_change < 0:
        print(f"{percentage_change:.2f}%")
    else:
        print(f"{percentage_change:.2f}%")

with open('tasas.json', 'r') as read_file:
    data = json.load(read_file)

source = data['source']

# Dollar rates

today = datetime.date.today().isoformat()
yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

dollar_today_buy = data[today]['currencies']['USD']['compra']
dollar_today_sell = data[today]['currencies']['USD']['venta']

dollar_yesterday_buy = data[today]['currencies']['USD']['compra']
dollar_yesterday_sell = data[today]['currencies']['USD']['venta']

# Euro rates
euro_today_buy = data[today]['currencies']['EUR']['compra']
euro_today_sell = data[today]['currencies']['EUR']['venta']

euro_yesterday_buy = data[yesterday]['currencies']['EUR']['compra']
euro_yesterday_sell = data[yesterday]['currencies']['EUR']['venta']

cambio_porcentual_venta_dollar = calculate_percentage_change(dollar_today_sell, dollar_yesterday_sell)
cambio_porcentual_compra_dollar = calculate_percentage_change(dollar_today_buy, dollar_yesterday_buy)

cambio_porcentual_venta_euro = calculate_percentage_change(euro_today_sell, euro_yesterday_sell)
cambio_porcentual_compra_euro = calculate_percentage_change(euro_today_buy, euro_yesterday_buy)

print_percentage_change(cambio_porcentual_venta_dollar)
print_percentage_change(cambio_porcentual_compra_dollar)
print_percentage_change(cambio_porcentual_venta_euro)
print_percentage_change(cambio_porcentual_compra_euro)