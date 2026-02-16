import os
import requests

from dotenv import load_dotenv
from typing import Any


def get_transaction_amount(transaction: dict[str, Any], date: str | None = None) -> float:
    """"""

    load_dotenv()

    operation_data = transaction.get("operationAmount", {})
    if operation_data.get('amount', "0") == "0":
        raise ValueError('Не найдены данные amount')

    operation_currency = operation_data.get("currency", {})
    if operation_currency.get('code', "0") == "0":
        raise ValueError('Не найдены данные currency.code')

    if operation_currency.get('name','0') == "0":
        raise ValueError('Не найдены данные currency.name')

    count = 0.0
    if operation_currency["code"] == "RUB":
        count = float(operation_data["amount"])
        return count

    #данные ключа
    api_key = os.getenv("API_KEY")
    header_data = {
        "apikey": api_key
    }

    # данные для конвертации валюты
    amount = operation_data["amount"]
    code_from = operation_currency["code"]
    code_to = "RUB"

    param = f"?to={code_to}&from={code_from}&amount={amount}"
    if not date is None:
        param += f"&date={date}"

    #ссылка на API
    api_http = "https://api.apilayer.com/exchangerates_data/convert"
    api_http += param

    response = requests.get(api_http, headers=header_data)

    status_code = response.status_code
    result_json = response.json()

    if not status_code == 200:
        return 0.0

    count =  float(result_json.get("result", "0.0"))
    return count
