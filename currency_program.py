import requests
def parse_rate(currency):
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rates = data["Valute"]
        if currency in rates:
            rate_value = rates[currency]["Value"]
            return rate_value
        else:
            return f"Курс для валюты {currency} не найден."
    else:
        return "Ошибка: " + str(response.status_code)

import telebot

bot = telebot.TeleBot("7036869107:AAEGcf1BDi8zpFOBw5jNWyTRXtV3pV9vQUo")

@bot.message_handler(func=lambda message: message.text.lower() == "курс" or message.text.lower() == "курс валют")
def handle_currency_request(message):
    bot.reply_to(message, "Введите код валюты (например, USD, EUR, HKD, GBP, CHF): ")
    bot.register_next_step_handler(message, parse_rate_input)

def parse_rate_input(message):
    currency = message.text.upper()
    exchange_rate = parse_rate(currency)
    bot.reply_to(message, f"Курс {currency}: {exchange_rate}")

if __name__ == "__main__":
    bot.polling()
