import pytest
import requests
import json
from ..requestsAPI import binance_api_requests

base_url = "https://api.binance.com"

#установливаем пару BTCUSDT для использования во всех тестах
@pytest.fixture
def symbol():
    return "BTCUSDT"

@pytest.fixture
def interval():
    return "1h"


# Проверка кода 200 и наличия ключа символов в списка всех доступных символов (торговых пар):
def test_get_all_symbols():
    response = binance_api_requests.get_all_symbols(base_url)
    assert response.status_code == 200
    exchange_info = response.json()
    assert "symbols" in exchange_info

# Проверка кода 200 и наличия ключей bids и asks в книге ордеров для конкретной пары:
def test_get_order_book(symbol):
    response = binance_api_requests.get_order_book(base_url, symbol)
    assert response.status_code == 200
    order_book = response.json()
    assert "bids" in order_book
    assert "asks" in order_book

# Проверка кода 200 и ответа - типа список для конкретной пары
def test_get_recent_trades(symbol):
    response = binance_api_requests.get_recent_trades(base_url, symbol)
    assert response.status_code == 200
    recent_trades = response.json()
    assert isinstance(recent_trades, list)

# Проверка кода 200 и ответа информации о свечах (candlesticks) - типа список при заданном интервале времени
def test_get_candlestick_data(symbol, interval):
    response = binance_api_requests.get_candlestick_data(base_url, symbol, interval)
    assert response.status_code == 200
    candlestick_data = response.json()
    assert isinstance(candlestick_data, list)

# Проверка кода 200, наличие цены в ответе для конкретной пары и принт в консоль значения цены для конкретной пары заданной выше в фикстуре
def test_get_symbol_price(symbol):
    response = binance_api_requests.get_symbol_price(base_url, symbol)
    assert response.status_code == 200
    symbol_price = response.json()
    assert "price" in symbol_price
    if response.status_code == 200:
        ticker_data = response.json()
        print("Price for", symbol, "is", ticker_data["price"])
    else:
        print("Error:", response.status_code, response.text)

# Проверка 401 ответа при неверном api-ключе (не авторизован)
def test_create_real_order_unathorized(symbol):
    api_secret = "incorrect_api_key_value"
    side = "BUY"
    type = "LIMIT"
    quantity = 0.01
    price = 9000

    response = binance_api_requests.create_real_order(base_url, api_secret, symbol, side, type, quantity, price)
    
    # Проверяем код состояния
    assert response.status_code == 401

    # Парсим JSON-ответ
    response_json = json.loads(response.text)

    # Проверяем, что "msg" содержит нужное сообщение о неверном формате API ключа
    assert "msg" in response_json
    assert response_json["msg"] == "API-key format invalid."

if __name__ == "__main__":
    pytest.main()