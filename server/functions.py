
def get_price(coin: str) -> float:
    import requests
    API_URL = 'https://api3.binance.com/api/v3/avgPrice'
    """
    :param coin: token name, e.g. BTC for Bitcoin, LTC for Litecoin
    :return: coin's current price in stable USDT. 1USDT ~ 1$ USA
    """
    data = {'symbol': f'{coin}USDT'}  # e.g. BTCUSDT
    response = requests.get(API_URL, data)

    return float(response.json()['price'])


if __name__ == '__main__':
    print(f"BCH = {get_price('BCH')} USD")
