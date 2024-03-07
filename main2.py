import openai
from lesson_schedule import get_schedule, get_today_schedule, get_schedule_tomorrow
from date_time import get_formatted_datetime
from weather import get_weather
from holidays import get_holiday_countdown
from currency_program import parse_rate
import quiz_program

openai.api_key = "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"

def main():
    print('''Вы можете управлять мной, отправляя следующие команды:

    "курс", "курс валют" - Получить текущий курс валюты.
    "расписание", "расписание уроков" - Получить расписание уроков.
    "расписание сегодня", "расписание на сегодня" - Получить расписание на текущий день.
    "дата и время", "дата", "время" - Получить текущую дату и время.
    "погода", "погода сейчас" - Получить текущую погоду в определенном городе.
    "праздники", "выходные", "ближайший праздник", "ближайшие выходные" - Получить информацию о ближайшем празднике или выходных.
    "викторина" - Сыграть в игру "викторина"
    "/help" - Получить команды для Чат-Бота.

    ИЛИ

    Любой запрос - Получить ответ на любой запрос до событий Сентября 2021 года.''')

    while True:
        user_input = input("Введите ваш запрос: ").strip().lower()

        try:
            if user_input == "курс" or user_input == "курс валют":
                currency = input("Введите код валюты (например, USD, EUR, HKD, GBP, CHF): ").upper()
                exchange_rate = parse_rate(currency)
                print(f"Курс {currency}: {exchange_rate}")
            elif user_input == "расписание" or user_input == "расписание уроков":
                schedule = get_schedule()
                print("Расписание уроков:")
                for day, lessons in schedule.items():
                    print(f"{day}: {', '.join(lessons)}")
            elif user_input == "расписание сегодня" or user_input == "расписание на сегодня":
                today_schedule = get_today_schedule()
                print("Расписание на сегодня:")
                if isinstance(today_schedule, list):
                    print(", ".join(today_schedule))
                else:
                    print(today_schedule)
            elif user_input == "расписание на завтра" or user_input == "расписание завтра":
                tomorrow_schedule = get_schedule_tomorrow()
                print("Расписание на завтра:")
                if isinstance(tomorrow_schedule, list):
                    print(", ".join(tomorrow_schedule))
                else:
                    print(tomorrow_schedule)
            elif user_input == "дата и время" or user_input == "дата" or user_input == "время":
                current_datetime = get_formatted_datetime()
                print(f"Текущая дата и время: {current_datetime}")
            elif user_input == "погода" or user_input == "погода сейчас":
                city = input("Введите название города: ")
                weather_info = get_weather(city)
                print(weather_info)
            elif user_input == "праздники" or user_input == "выходные" or user_input == "ближайший праздник" or user_input == "ближайшие выходные" or user_input == "праздник" or user_input == "близжайший праздник" or user_input == "близжайший праздник":
                holiday, holiday_date, days_until_holiday = get_holiday_countdown()
                if holiday:
                    print(f"Ближайший праздник: {holiday}, Дата: {holiday_date}, Дней до праздника: {days_until_holiday}")
                else:
                    print("Ближайшие праздники не найдены.")
            elif user_input == "help" or user_input == "/help":
                return main()
            elif user_input in ["викторина", "игра", "давай поиграем", "запусти игру", "запусти викторину"]:
                print("Запускаю викторину...")
                quiz_program.main()
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
                print(response['choices'][0]['message']['content'].strip())

        except Exception as e:
            error_message = str(e)
            if "Rate limit reached" in error_message:
                print("Превышено количество запросов. Повторите через 20 секунд.")
            else:
                print(f"Произошла ошибка: {error_message}")

if __name__ == "__main__":
    main()
