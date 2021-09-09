import urllib.request
import json
import pandas as pd


def request():
    url = "https://api.nomics.com/v1/currencies/ticker?key=e28a984356c35fd8a210e5a656ef190f385a9f9e&ids=BTC,ETH,HEX,ADA,BNB,USDT,XRP,SOL,DOGE,DOT,USDC,UNI,LTC,LINK,BCH,LUNA,BUSD,ICP,FTXTOKEN,MATIC,VET,WBTC,ETC,XLM,FIL,AVAX,THETA,CETH,TRX,ALGO,ATOM,BCHA,DAI&interval=1d,7d,30d,365d,ytd&convert=EUR&per-page=100&page=1"
    response = urllib.request.urlopen(url)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8')
    with open('crypto_data.json', 'w') as crypto_file_pointer:
        crypto_file_pointer.write(text)


def create_df():
    with open('crypto_data.json', 'r') as file_pointer:
        data = json.load(file_pointer)

    df = pd.json_normalize(data)
    pd.set_option('display.max_columns', None)
    # print(df.head())
    return df


# request()
create_df()