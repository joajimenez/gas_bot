from datetime import datetime
import json
import locale
from typing import Final

from dotenv import dotenv_values
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    filters,
    MessageHandler,
)

import calculadora

# Load API key from .env file

env_variables = dotenv_values(".env")
TELEGRAM_API_KEY = env_variables['TELEGRAM_API_TOKEN']

TOKEN: Final = TELEGRAM_API_KEY
BOT_USERNAME: Final = '@gas_rd_bot'

# Import, format and display FUEL prices from json file.

with open('fuel_prices.json', 'r') as read_file:
    data = json.load(read_file)

prices = data['prices']


# Set locale to "es-DO"
locale.setlocale(locale.LC_TIME, 'es_DO.utf8')

last_update_date = data['date']
date_object = datetime.strptime(last_update_date, "%Y-%m-%d")
formatted_date = date_object.strftime("%d de %B, %Y").capitalize()

# print(last_update_date)

formatted_keys = {
    'gasolina_premium': 'Gasolina Premium',
    'gasolina_regular': 'Gasolina Regular',
    'diesel_premium': 'Diesel Premium',
    'diesel_regular': 'Diesel Regular',
    'avtur': 'Avtur',
    'keroseno': 'Keroseno',
    'fuel_oil_#6': 'Fuel Oil #6',
    'fuel_oil_1%': 'Fuel Oil 1%',
    'glp': 'GLP',
    'gas_natural': 'Gas Natural'
}

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hola, soy un bot que te da los precios actualizados '
                                    'de los combustibles en RD.  Haz click en MENU '
                                    'para ver las opciones. Desarrollado por @Pyre_3.')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Aun estoy en desarrollo. Por el momento solo puedo dar los precios de los combustibles cuando haces click en el botón de /PRECIOS.')

async def fuel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    formatted_prices = '\n'.join([f"* {formatted_keys[key]}: ${value:.2f}" for key, value in prices.items()])
    response = f'Precios al {formatted_date}:\n\n{formatted_prices}'
    await update.message.reply_text(response)
    

# DONE: Fix percentage change display
    
async def currency_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  
    response = f'Tasas del dia:\n\n**DOLAR:\nCompra: ${calculadora.dollar_compra_hoy:.2f}\nVenta: ${calculadora.dollar_venta_hoy:.2f}\nCambio porcentual vs ayer: {calculadora.cambio_porcentual_compra_dollar:.2f}%\n\n**EURO:\nCompra: ${calculadora.euro_compra_hoy:.2f}\nVenta: ${calculadora.euro_venta_hoy:.2f}\nCambio porcentual vs ayer: {calculadora.cambio_porcentual_compra_euro:.2f}%\n\nFuente: {calculadora.source}'
    await update.message.reply_text(response)


# Responses

def handle_response(text: str):
    processed_text: str = text.lower()
    if 'hello' in processed_text or 'hola' in processed_text:
        return 'klk manito!'

    if 'como estas' in processed_text:
        return "Tamo bien!"

    if 'amo la republica dominicana' in processed_text or 'amo errede' in processed_text or 'amo rd' in processed_text or 'errede' in processed_text:
        return 'Amo la Republica Dominicana!'
    
    if 'gracias' in processed_text:
        return 'De nada!'

    return 'No entiendo lo que escribiste...'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type}: '{text}")

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('inicio', start_command))
    app.add_handler(CommandHandler('ayuda', help_command))
    app.add_handler(CommandHandler('precios', fuel_command))
    app.add_handler(CommandHandler('tasas_del_dia', currency_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot (listen for messages)
    print('Polling...')
    app.run_polling(poll_interval=5)
    
    # Dotenv file for API keys and other sensitive info (not included in repo) 
    print(TELEGRAM_API_KEY)
