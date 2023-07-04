import json

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
dollar_compra_hoy = data['currencies']['dollar']['compra']
dollar_venta_hoy = data['currencies']['dollar']['venta']

dollar_compra_ayer = 55.25
dollar_venta_ayer = 55.57

# Euro rates
euro_compra_hoy = data['currencies']['euro']['compra']
euro_venta_hoy = data['currencies']['euro']['venta']

euro_compra_ayer = 59.25
euro_venta_ayer = 62.57

cambio_porcentual_venta_dollar = calculate_percentage_change(dollar_venta_hoy, dollar_venta_ayer)
cambio_porcentual_compra_dollar = calculate_percentage_change(dollar_compra_hoy, dollar_compra_ayer)

cambio_porcentual_venta_euro = calculate_percentage_change(euro_venta_hoy, euro_venta_ayer)
cambio_porcentual_compra_euro = calculate_percentage_change(euro_compra_hoy, euro_compra_ayer)

print_percentage_change(cambio_porcentual_venta_dollar)
print_percentage_change(cambio_porcentual_compra_dollar)
print_percentage_change(cambio_porcentual_venta_euro)
print_percentage_change(cambio_porcentual_compra_euro)