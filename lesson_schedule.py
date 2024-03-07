def get_schedule():
    schedule = {
        "Понедельник": ["Физика", "Физ-ра", "Математика", "Физика", "Индивидуальный проект", "Лит-ра", "Ук Математика профиль"],
        "\nВторник": ["Математика", "Математика", "ОБЖ", "История", "Ук Математика профиль"],
        "\nСреда": ["Литература", "Математика", "Английский", "Ук математика база", "Ук информатика"],
        "\nЧетверг": ["Лит-ра", "Математика", "Английский", "История", "Математика"],
        "\nПятница": ["Родной язык", "Русский", "Ук информатика"],
        "\nСуббота": ["Русский", "Лит-ра", "Английский", "Физ-ра", "Ук компьютерная графика"]
    }
    return schedule

import datetime

def get_today_schedule():
    days_mapping = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье"
    }

    current_day_index = datetime.datetime.now().weekday()
    current_day = days_mapping[current_day_index]

    schedule = get_schedule()
    today_schedule = schedule.get("\n" + current_day, "На сегодня расписания нет.")

    return today_schedule

def get_schedule_tomorrow():
    days_mapping = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье"
    }

    tomorrow_index = (datetime.datetime.now().weekday() + 1) % 7
    tomorrow = days_mapping[tomorrow_index]

    schedule = get_schedule()
    tomorrow_schedule = schedule.get("\n" + tomorrow, "На завтра расписания нет.")

    return tomorrow_schedule
