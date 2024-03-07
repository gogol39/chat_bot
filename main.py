import telebot
import openai
from lesson_schedule import get_schedule, get_today_schedule, get_schedule_tomorrow
from date_time import get_formatted_datetime
from weather import get_weather
from holidays import get_holiday_countdown
from currency_program import parse_rate

openai.api_key = "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"
bot = telebot.TeleBot("7036869107:AAEGcf1BDi8zpFOBw5jNWyTRXtV3pV9vQUo")

def get_exchange_rate(currency):
    pass

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, '''Вы можете управлять мной, отправляя следующие команды:

"курс", "курс валют" - Получить текущий курс валюты.
"расписание", "расписание уроков" - Получить расписание уроков.
"расписание сегодня", "расписание на сегодня" - Получить расписание на текущий день.
"дата и время", "дата", "время" - Получить текущую дату и время.
"погода", "погода сейчас" - Получить текущую погоду в определенном городе.
"праздники", "выходные", "ближайший праздник", "ближайшие выходные" - Получить информацию о ближайшем празднике или выходных.
"/help" - Получить команды для Чат-Бота.

ИЛИ

Любой запрос - Получить ответ на любой запрос до событий Сентября 2021 года.''')

@bot.message_handler(func=lambda message: message.text.lower() == "курс" or message.text.lower() == "курс валют")
def handle_currency_request(message):
    bot.reply_to(message, "Введите код валюты (например, USD, EUR, HKD, GBP, CHF): ")
    bot.register_next_step_handler(message, parse_rate_input)

@bot.message_handler(commands=['help'])
def start(message):
    bot.reply_to(message, '''Вы можете управлять мной, отправляя следующие команды:

"курс", "курс валют" - Получить текущий курс валюты.
"расписание", "расписание уроков" - Получить расписание уроков.
"расписание сегодня", "расписание на сегодня" - Получить расписание на текущий день.
"дата и время", "дата", "время" - Получить текущую дату и время.
"погода", "погода сейчас" - Получить текущую погоду в определенном городе.
"праздники", "выходные", "ближайший праздник", "ближайшие выходные" - Получить информацию о ближайшем празднике или выходных.
"/help" - Получить команды для Чат-Бота.

ИЛИ

Любой запрос - Получить ответ на любой запрос до событий Сентября 2021 года.''')
def parse_rate_input(message):
    currency = message.text.upper()
    exchange_rate = parse_rate(currency)
    bot.reply_to(message, f"Курс {currency}: {exchange_rate}")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text.lower()

    try:
        if user_input == "выход":
            bot.reply_to(message, "До свидания!")
            return

        if user_input == "расписание" or user_input.lower() == "расписание уроков":
            schedule = get_schedule()
            response = "Расписание уроков:\n\n"
            for day, lessons in schedule.items():
                response += f"{day}: {', '.join(lessons)}\n"
            bot.reply_to(message, response)
        elif user_input == "расписание сегодня" or user_input.lower() == "расписание на сегодня":
            today_schedule = get_today_schedule()
            response = "Расписание на сегодня:\n"

            if isinstance(today_schedule, list):
                response += ", ".join(today_schedule)

            else:
                response += today_schedule
            bot.reply_to(message, response)
        elif user_input == "расписание на завтра" or user_input.lower() == "расписание завтра":
            tomorrow_schedule = get_schedule_tomorrow()
            response = "Расписание на завтра:\n"
            if isinstance(tomorrow_schedule, list):
                response += ", ".join(tomorrow_schedule)
            else:
                response += tomorrow_schedule
            bot.reply_to(message, response)

        elif user_input == "дата и время" or user_input.lower() == "дата" or user_input.lower() == "время":
            current_datetime = get_formatted_datetime()
            bot.reply_to(message, f"Текущая дата и время: {current_datetime}")
        elif user_input == "погода" or user_input.lower() == "погода сейчас":
            bot.reply_to(message, "Введите название города:")
            bot.register_next_step_handler(message, handle_weather_input)
        elif user_input == "праздники" or user_input.lower() == "выходные" or user_input.lower() == "ближайший праздник" or user_input.lower() == "ближайшие выходные" or user_input.lower() == "праздник" or user_input.lower() == "близжайший праздник" or user_input.lower() == "близжайший праздник":
            holiday, holiday_date, days_until_holiday = get_holiday_countdown()
            if holiday:
                bot.reply_to(message, f"Ближайший праздник: {holiday}, Дата: {holiday_date}, Дней до праздника: {days_until_holiday}")
            else:
                bot.reply_to(message, "Ближайшие праздники не найдены.")
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Вы общаетесь с чат-ботом."},
                    {"role": "user", "content": user_input},
                ],
                temperature=0.5,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.5,
                presence_penalty=0.0,
            )
            bot.reply_to(message, response['choices'][0]['message']['content'].strip())

    except Exception as e:
        error_message = str(e)
        if "Rate limit reached" in error_message:
            bot.reply_to(message, "Превышено количество запросов. Повторите через 20 секунд.")
        else:
            bot.reply_to(message, f"Произошла ошибка: {error_message}")

def handle_weather_input(message):
    city = message.text
    weather_info = get_weather(city)
    bot.reply_to(message, weather_info)

if __name__ == "__main__":
    bot.polling()
