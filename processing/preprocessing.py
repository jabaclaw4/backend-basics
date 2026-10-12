# порог температуры в градусах, ниже которого нужна тёплая одежда
WARM_CLOTHES_THRESHOLD_C = 0
# порог курса к рублю, выше которого курс считается дорогим
EXPENSIVE_RATE_THRESHOLD = 100
# описание погоды по умолчанию, если сервис его не вернул
DEFAULT_DESCRIPTION = "нет данных"


def is_warm_clothes_needed(temp_c: float) -> bool:
    return temp_c < WARM_CLOTHES_THRESHOLD_C


def is_expensive(rate: float) -> bool:
    return rate > EXPENSIVE_RATE_THRESHOLD


def normalize_description(description: str | None) -> str:
    if description is None or not description.strip():
        return DEFAULT_DESCRIPTION
    return description.strip()