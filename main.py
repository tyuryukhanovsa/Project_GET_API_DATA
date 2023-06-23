from datetime import datetime
import requests
import json

import os

API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
CURRENCY_RATES_FILE = 'carrency_rate.json'


def main():
    while True:
        carrency = input('Введите название валюты (USD или EUR): ').upper()
        if carrency not in ('USD', 'EUR'):
            print('Некорректный ввод')
            continue

        rate = get_carrency_rate(carrency)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'Курс валюты {carrency} к рублю: {rate}')

        data = {'carrency': carrency, 'rate': rate, 'timestamp': timestamp}
        save_to_json(data)

        choice = input('Выберите действие: (1-продолжить, 2-выйти) ')
        if choice == '1':
            continue
        elif choice == '2':
            break
        else:
            print('Неизвестная команда')

def get_carrency_rate(carrency: str) -> float:
    """Получает курс от API и возвращает float"""
    url = f"https://api.apilayer.com/currency_data/live?source={carrency}"

    response = requests.get(url, headers={"apikey": API_KEY})
    carrency_key = carrency + 'RUB'
    rate = response.json()['quotes'][f'{carrency_key}']
    return rate

def save_to_json(data: dict) -> None:
    """Сохраняет данный в json файл"""
    with open(CURRENCY_RATES_FILE, 'a') as f:
        if os.stat(CURRENCY_RATES_FILE).st_size == 0:
            json.dump([data], f)
        else:
            with open(CURRENCY_RATES_FILE, 'r') as f:
                data_list = json.load(f)
                data_list.append(data)
            with open(CURRENCY_RATES_FILE, 'w') as f:
                json.dump(data_list, f)
    pass

if __name__ == "__main__":
    main()