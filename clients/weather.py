from clients.http import get_with_retry, parse_json
from exceptions import NotFoundError, ServiceUnavailableError

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# расшифровка кодов погоды WMO, которые отдаёт Open-Meteo
WEATHER_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "slight snow fall",
    73: "moderate snow fall",
    75: "heavy snow fall",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    95: "thunderstorm",
}


def _find_coordinates(city: str) -> tuple[float, float]:
    # геокодинг: название города превращаем в координаты
    response = get_with_retry(
        GEOCODING_URL,
        params={"name": city, "count": 1, "language": "en", "format": "json"},
    )
    data = parse_json(response)
    results = data.get("results")
    if not results:
        raise NotFoundError(f"город не найден: {city}")
    latitude = results[0].get("latitude")
    longitude = results[0].get("longitude")
    if latitude is None or longitude is None:
        raise ServiceUnavailableError("в ответе геокодинга нет координат")
    return latitude, longitude


def get_weather(city: str) -> dict:
    latitude, longitude = _find_coordinates(city)
    response = get_with_retry(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,weather_code",
        },
    )
    data = parse_json(response)
    current = data.get("current")
    if not isinstance(current, dict):
        raise ServiceUnavailableError("в ответе прогноза нет блока current")
    temp = current.get("temperature_2m")
    if not isinstance(temp, (int, float)):
        raise ServiceUnavailableError("в ответе прогноза нет температуры")
    # неизвестный код даёт пустое описание, значение по умолчанию подставит предобработка
    description = WEATHER_CODES.get(current.get("weather_code"), "")
    return {"temp_c": float(temp), "description": description}