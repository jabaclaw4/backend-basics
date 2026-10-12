from clients.rates import get_rate
from clients.weather import get_weather
from processing.preprocessing import (
    is_expensive,
    is_warm_clothes_needed,
    normalize_description,
)


def build_city_summary(city: str, currency: str = "USD") -> dict:
    weather = get_weather(city)
    rate = get_rate(currency)
    return {
        "city": city,
        "weather": {
            "temp_c": weather["temp_c"],
            "description": normalize_description(weather["description"]),
            "warm_clothes": is_warm_clothes_needed(weather["temp_c"]),
        },
        "rates": {
            "currency": currency.strip().upper(),
            "rate_to_rub": rate,
            "expensive": is_expensive(rate),
        },
    }