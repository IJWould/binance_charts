import logging

import time
from datetime import datetime, timezone

from binance.lib.utils import config_logging

from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
from binance.websocket.websocket_client import BinanceWebsocketClient
from binance.websocket.binance_socket_manager import BinanceSocketManager

from binance.spot import Spot
from binance.spot._market import ui_klines
from binance.spot._trade import account

from creation_json import create_json_file

from prepare_env import get_api_key

from flask import Flask, render_template, url_for, redirect, jsonify
from flask_socketio import SocketIO, emit
from Flask_wtf_forms import crypto_char

from websocket import WebSocketApp, create_connection



api_key, api_secret = get_api_key()

api_client = Spot(api_key=api_key, api_secret=api_secret)
_book_ticker = api_client.book_ticker()

_filter = list(filter(lambda pair: float(pair['bidPrice']) > 0 and 'USDT' in pair['symbol'], _book_ticker))

stream_client = SpotWebsocketStreamClient()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yo432u-will-n5sdf23e321ver-g34u3e321ss'


base_endpoint = 'wss://stream.binance.com:9443/ws/'

# def format_timestamp(milliseconds, timeframe):
#     # Convert milliseconds to seconds
#     seconds = milliseconds / 1000.0
#     # Create a datetime object in UTC
#     date = datetime.fromtimestamp(seconds)

#     # Format the date to the desired string format
#     return date.strftime('%Y-%m-%dT%H:%M:%S')




@app.route('/', methods=['GET', 'POST'])
def index():

    form = crypto_char()
    return render_template('index.html',tickers=_filter)


'''json



    dates'''

@app.route('/history/<pair>/<timeframe>')
def candles_js(pair, timeframe):

    candle_stick = []

    volume_diagramm = []

    klines_data = api_client.klines(pair.upper(), timeframe, limit=1000)
    for value in klines_data:



        candle={
            "time": value[0] / 1000,
            'open': value[1],
            'high': value[2],
            'low': value[3],
            'close': value[4],


        }

        # volume = {
        #     "time": value[0] / 1000,
        #     'volume': value[5],
        #     "color": '#26a69a',
        #     # 'Quote_asset_volume': value[7],
        #     # 'Taker_buy_base_asset_volume': value[9],
        #     # 'Taker_buy_quote_asset_volume': value[10]
        # }

        # volume_diagramm.append(volume)


        candle_stick.append(candle)
    return jsonify(candle_stick)


# @app.route('/history1/<pair>/<timeframe>')
# def candles_js0(pair, timeframe):

#     formatted_data = []

#     klines_data = api_client.klines(pair.upper(), timeframe)
#     for value in klines_data:



#         candle={
#             "time": value[0] / 1000,
#             'open': value[1],
#             'high': value[2],
#             'low': value[3],
#             'close': value[4]
#             }
#         formatted_data.append(candle)
#
#     return jsonify(formatted_data)
# @app.route('/history2/<pair>/<timeframe>')
# def candles_js1(pair, timeframe):

#     formatted_data = []

#     klines_data = api_client.klines(pair.upper(), timeframe)
#     for value in klines_data:



#         candle={
#             "time": value[0] / 1000,
#             'open': value[1],
#             'high': value[2],
#             'low': value[3],
#             'close': value[4]
#             }
#         formatted_data.append(candle)

#     return jsonify(formatted_data)

# @app.route('/history3/<pair>/<timeframe>')
# def candles_js2(pair, timeframe):

#     formatted_data = []

#     klines_data = api_client.klines(pair.upper(), timeframe)
#     for value in klines_data:



#         candle={
#             "time": value[0] / 1000,
#             'open': value[1],
#             'high': value[2],
#             'low': value[3],
#             'close': value[4]
#             }
#         formatted_data.append(candle)

#     return jsonify(formatted_data)

@app.route('/analytics')
def analytics():

    return 'asd'

@app.route('/news')
def news():

    return 'asd'


app.run(debug=True)