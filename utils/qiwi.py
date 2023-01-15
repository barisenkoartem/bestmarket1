import json
import requests

from random import choices
from string import ascii_uppercase, digits

import config


def generate_billid(length: int) -> str:
    return "".join(choices(ascii_uppercase + digits, k=length))


def get_invoice(amount: float):
    billid = generate_billid(6)
    s = requests.Session()
    s.headers['Accept'] = 'application/json'
    s.headers['Authorization'] = 'Bearer ' + config.SECRET_QIWI_TOKEN
    s.headers['Content-Type'] = 'application/json'
    p = {
        "amount": {
            "currency": "RUB",
            "value": f"{amount}"
        },
        "expirationDateTime": "2025-12-10T09:02:00+03:00",
    }
    payload = json.dumps(p)
    link = f'https://api.qiwi.com/partner/bill/v1/bills/{billid}'
    response = s.put(url=link, data=payload)
    return response.json()


def is_bill_paid(billid: str):
    s = requests.Session()
    s.headers['Accept'] = 'application/json'
    s.headers['Authorization'] = 'Bearer ' + config.SECRET_QIWI_TOKEN
    link = f'https://api.qiwi.com/partner/bill/v1/bills/{billid}'
    response = s.get(url=link)
    status = response.json()['status']['value']
    if status == "PAID":
        return True
    else:
        return False