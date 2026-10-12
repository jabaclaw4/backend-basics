import argparse
import json
import sys

from exceptions import NotFoundError, ServiceUnavailableError
from processing.service import build_city_summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="сводка по городу: погода и курс валюты")
    parser.add_argument("--city", required=True, help="название города, например Moscow")
    parser.add_argument("--currency", default="USD", help="код валюты, по умолчанию USD")
    parser.add_argument("--json", action="store_true", help="вывести сводку в формате JSON")
    args = parser.parse_args()
    if not args.city.strip():
        parser.error("--city не может быть пустым")
    return args


def format_summary(summary: dict) -> str:
    weather = summary["weather"]
    rates = summary["rates"]
    lines = [
        f"Город: {summary['city']}",
        f"Погода: {weather['temp_c']}°C, {weather['description']}",
        f"Тёплая одежда: {'да' if weather['warm_clothes'] else 'нет'}",
        f"{rates['currency']} - RUB: {rates['rate_to_rub']:.2f}",
        f"Дорогой курс: {'да' if rates['expensive'] else 'нет'}",
    ]
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        summary = build_city_summary(args.city, args.currency)
    except NotFoundError as error:
        print(error, file=sys.stderr)
        return 3
    except ServiceUnavailableError as error:
        print(error, file=sys.stderr)
        return 4
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(format_summary(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())