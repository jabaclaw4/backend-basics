import time

from clients.http import get_with_retry, parse_json
from exceptions import NotFoundError, ServiceUnavailableError

RATES_URL = "https://api.frankfurter.dev/v2/rate"

# время жизни кэша курса в секундах
CACHE_TTL = 300

# кэш: {код валюты: (курс, момент сохранения)}
_cache: dict[str, tuple[float, float]] = {}


def _get_cached(code: str) -> float | None:
    # возвращает курс из кэша, если он ещё свежий
    entry = _cache.get(code)
    if entry is None:
        return None
    rate, saved_at = entry
    if time.monotonic() - saved_at >= CACHE_TTL:
        # запись устарела, убираем её
        _cache.pop(code, None)
        return None
    return rate


def _put_cache(code: str, rate: float) -> None:
    _cache[code] = (rate, time.monotonic())


def get_rate(currency: str) -> float:
    code = currency.strip().upper()
    if not code.isalpha():
        raise NotFoundError(f"валюта не найдена: {currency}")

    # сначала смотрим кэш
    cached = _get_cached(code)
    if cached is not None:
        return cached

    response = get_with_retry(f"{RATES_URL}/{code}/RUB")
    # неизвестный код валюты сервис отвечает 422 (на всякий случай и 404)
    if response.status_code in (404, 422):
        raise NotFoundError(f"валюта не найдена: {code}")
    data = parse_json(response)
    rate = data.get("rate")
    if not isinstance(rate, (int, float)):
        raise ServiceUnavailableError("в ответе курса нет числового поля rate")
    result = float(rate)

    _put_cache(code, result)
    return result