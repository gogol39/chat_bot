import requests

def get_weather(city):
    api_key = "2b011c8c9ff6ca33c7d42cdd13354199"

    weather_translations = {
        "clear sky": "ясно",
        "few clouds": "малооблачно",
        "scattered clouds": "переменная облачность",
        "broken clouds": "облачно с прояснениями",
        "shower rain": "идёт сильный дождь",
        "rain": "идёт дождь",
        "thunderstorm": "гроза",
        "snow": "снегопад",
        "mist": "туман"
    }
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            weather_description_key = data["weather"][0]["description"]
            weather_description = weather_translations.get(weather_description_key, "недоступно")
            temperature = round(data["main"]["temp"])  # Округляем температуру до целого числа
            temperature_sign = "+" if temperature >= 0 else ""  # Добавляем знак перед температурой
            return f"Погода в городе {city}: {weather_description}. Температура: {temperature_sign}{temperature}°C"
        else:
            return "Не удалось получить информацию о погоде"
    except Exception as e:
        return f"Произошла ошибка при получении погоды: {str(e)}"