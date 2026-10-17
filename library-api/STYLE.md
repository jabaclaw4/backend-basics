# Стиль API

Правила оформления, которых придерживается Library API.

1. **URL в kebab-case.** Пример: `/loans/{id}/return`. Не используем camelCase или snake_case в путях.
2. **JSON в snake_case.** Пример: `full_name`, `book_id`, `published_year`.
3. **Версия API в `servers`.** Базовый URL содержит `/v1/`: `https://api.example.com/v1`.
4. **Идентификатор ресурса — в path.** Пример: `GET /books/15`. Не используем `GET /books?id=15`.
5. **Фильтры и сортировка — в query.** Пример: `GET /loans?status=overdue&sort=-due_date`.
6. **Единый формат ошибок.** Все ошибки возвращают `ErrorResponse` с полями `code`, `message`, `details`, `request_id`.
7. **Коды ответов.** На создание — `201`, на удаление — `204`, на отсутствие ресурса — `404`, на нарушение бизнес-правила — `409`, на ошибку валидации — `422`.
8. **Обязательные поля в `required`.** Клиент обязан передать эти поля, иначе сервер вернет ошибку.
9. **ReadOnly-поля не отправляются клиентом.** Поля `id`, `available_copies`, `registered_at`, `loaned_at`, `returned_at` возвращает только сервер.
10. **`Idempotency-Key` на опасные POST.** Для `POST /loans` обязателен заголовок `Idempotency-Key` с UUID для защиты от дублей при повторной отправке.