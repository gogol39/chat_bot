from datetime import datetime

holidays = {
    "Новогодние каникулы": [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (8, 1)],
    "Рождество Христово": [(7, 1)],
    "День защитника Отечества": [(23, 2)],
    "Международный женский день": [(8, 3)],
    "Праздник Весны и Труда": [(1, 5)],
    "День Победы": [(9, 5)],
    "День России": [(12, 6)],
    "День народного единства": [(4, 11)]
}

def get_holiday_countdown():
    current_date = datetime.now().date()
    for holiday, dates in holidays.items():
        for date_tuple in dates:
            holiday_date = datetime(current_date.year, date_tuple[1], date_tuple[0]).date()
            if holiday_date >= current_date:
                days_until_holiday = (holiday_date - current_date).days
                return holiday, holiday_date, days_until_holiday

    return None, None, None
