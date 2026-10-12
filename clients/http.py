import time

import requests

from exceptions import ServiceUnavailableError

# таймаут одного запроса в секундах
TIMEOUT = 10
# сколько повторов делаем после первой попытки
RETRIES = 2
# временные ошибки сервера, при которых повторяем запрос
RETRY_STATUSES = {500, 502, 503, 504}
# базовая пауза между попытками в секундах, растёт вдвое с каждой попыткой
BACKOFF = 1
# верхняя граница паузы, чтобы огромный Retry-After не завесил программу
MAX_DELAY = 30


def _retry_after_delay(response: requests.Response, fallback: float) -> float:
    # берём число секунд из Retry-After, если заголовок есть и это число
    value = response.headers.get("Retry-After", "")
    if value.isdigit():
        return min(int(value), MAX_DELAY)
    return fallback


def get_with_retry(url: str, params: dict | None = None) -> requests.Response:
    last_error = "неизвестная ошибка"
    for attempt in range(1 + RETRIES):
        delay = BACKOFF * 2 ** attempt
        try:
            response = requests.get(url, params=params, timeout=TIMEOUT)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as error:
            last_error = f"сетевая ошибка: {error}"
        else:
            if response.status_code in RETRY_STATUSES:
                last_error = f"статус {response.status_code}"
            elif response.status_code == 429:
                last_error = "статус 429 (слишком много запросов)"
                delay = _retry_after_delay(response, delay)
            else:
                # успех или ошибка клиента: решает вызывающий код
                return response
        # после последней попытки не ждём
        if attempt < RETRIES:
            time.sleep(delay)
    raise ServiceUnavailableError(f"сервис недоступен ({url}): {last_error}")


def parse_json(response: requests.Response) -> dict:
    # проверяем статус и формат ответа, любое отклонение превращаем в понятную ошибку
    if response.status_code != 200:
        raise ServiceUnavailableError(
            f"неожиданный статус {response.status_code} от {response.url}"
        )
    try:
        data = response.json()
    except ValueError:
        raise ServiceUnavailableError(f"ответ {response.url} не является JSON")
    if not isinstance(data, dict):
        raise ServiceUnavailableError(f"неожиданный формат ответа {response.url}")
    return data