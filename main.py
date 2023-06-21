import os

value = os.environ.get('EXCHANGE_RATE_API_KEY')


if __name__ == '__main__':
    print(value)