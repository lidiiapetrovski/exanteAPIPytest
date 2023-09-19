import requests
import hashlib
import hmac
import time

# Получение списка всех доступных символов (торговых пар):
def get_all_symbols(base_url):
    endpoint = "/api/v3/exchangeInfo"
    response = requests.get(base_url + endpoint)
    return response

# Получение информации о книге ордеров для конкретной пары:
def get_order_book(base_url, symbol):
    endpoint = "/api/v3/depth"
    params = {"symbol": symbol}
    response = requests.get(base_url + endpoint, params=params)
    return response

# Получение последних сделок для конкретной пары
def get_recent_trades(base_url, symbol):
    endpoint = "/api/v3/trades"
    params = {"symbol": symbol}
    response = requests.get(base_url + endpoint, params=params)
    return response

# Получение информации о свечах (candlesticks)
def get_candlestick_data(base_url, symbol, interval):
    endpoint = "/api/v3/klines"
    params = {"symbol": symbol, "interval": interval}
    response = requests.get(base_url + endpoint, params=params)
    return response

# Получение информации о цене для конкретной пары
def get_symbol_price(base_url, symbol):
    endpoint = "/api/v3/ticker/price"
    params = {"symbol": symbol}
    response = requests.get(base_url + endpoint, params=params)
    return response

# Создание ордера 
def create_real_order(base_url, api_secret, symbol, side, type, quantity, price):
    endpoint = "/api/v3/order"  

    params = {
        "symbol": symbol,
        "side": side,
        "type": type,
        "quantity": quantity,
        "price": price,  # Укажите желаемую цену для покупки
        "timestamp": int(time.time() * 1000)  # Текущее время в миллисекундах
    }

    # Формирование строки для подписи
    query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
    
    # Создание подписи HMAC-SHA256
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    # Добавление подписи и API ключа к заголовкам запроса
    headers = {
        "X-MBX-APIKEY": "test"
    }

    # Добавление подписи к параметрам запроса
    params['signature'] = signature

    # Выполнение POST-запроса с параметрами и подписью
    response = requests.post(base_url + endpoint, params=params, headers=headers)
    
    return response
