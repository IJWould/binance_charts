import csv
import json

from binance.spot import Spot
from binance.spot._market import ui_klines

from prepare_env import get_api_key
from datetime import datetime


api_key, api_secret = get_api_key()
api_client = Spot(api_key=api_key, api_secret=api_secret)






def create_json_file(symbol_of_crypto: str, interval: str):
    """
            interval:
        m -> minutes; h -> hours; d -> days; w -> weeks; M -> months

        - 1m
        - 3m
        - 5m
        - 15m
        - 30m
        - 1h
        - 2h
        - 4h
        - 6h
        - 8h
        - 12h
        - 1d
        - 3d
        - 1w
        - 1M

    """




    file_path = f'intervals_data_time/{symbol_of_crypto}_{interval}.json'

    formatted_data = []
    klines_data = api_client.ui_klines(symbol_of_crypto.upper(), interval)

    for value in klines_data:



        candle={
            "time": value[0],
            'open': value[1],
            'high': value[2],
            'low': value[3],
            'close': value[4],
            }
        formatted_data.append(candle)

    with open(file_path, 'w') as file:

        json.dump(formatted_data, file,indent=2)



