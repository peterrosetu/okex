from idc import *
import requests,os
from okx import *

passphrase = ""
api_key = 'e9115b9c-ffa3-4b6c-97ac-ee8f9e458458'
secret_key = 'D3BC88FB1FDDB57B7FDF1E1C90445725'

os.environ["http_proxy"] = "http://127.0.0.1:10809"
os.environ["https_proxy"] = "http://127.0.0.1:10809"

flag = '1' # 0 is real , 1 is simulate

accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)

print(accountAPI)

result = accountAPI.get_account('BTC')

print(result)

'''
url_pub = "wss://ws.okx.com:8443/ws/v5/public?brokerId=9999" # public channel

url_pri = "wss://ws.okx.com:8443/ws/v5/private?brokerId=9999" #private channel

loop.run_until_complete(subscribe_without_login(url_pub, channels))	# 公共频道 不需要登录（行情，持仓总量，K线，标记价格，深度，资金费率等）

loop.run_until_complete(subscribe(url_pri, api_key, passphrase, secret_key, channels)) 	# 私有频道 需要登录（账户，持仓，订单等）

loop.run_until_complete(trade(url_pri, api_key, passphrase, secret_key, trade_param)) # 交易（下单，撤单，改单等）
'''

