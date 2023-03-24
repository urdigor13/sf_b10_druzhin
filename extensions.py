import requests
import json

from config import exchanges, APILAYER_TOKEN

class APIException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        payload = {}
        headers = {
            # "apikey": "aipgepmU4DTT8l4dqLr9w9Jf8dN2FTUG"
            "apikey": APILAYER_TOKEN
        }
        url = f"https://api.apilayer.com/exchangerates_data/latest?base={base_key}&symbols={sym_key}"
        requests.packages.urllib3.disable_warnings()
        r = requests.request("GET", url, headers=headers, data=payload, verify=False)
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * float(amount)
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return new_price #message