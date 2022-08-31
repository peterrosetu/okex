import json,sys,csv,time,os
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import okx.Account_api as Account
import okx.Funding_api as Funding
import okx.Market_api as Market
import okx.Public_api as Public
import okx.Trade_api as Trade
import okx.status_api as Status
import okx.subAccount_api as SubAccount
import okx.TradingData_api as TradingData
import okx.Broker_api as Broker
os.environ["http_proxy"] = "http://127.0.0.1:10809"
os.environ["https_proxy"] = "http://127.0.0.1:10809"

def read_key():	
	if os.path.isfile('setting/key.csv') == False:
		return None		
	df = pd.read_csv('setting/key.csv', dtype='str', engine='python')
	df['time_key'] = df.index
	return(df)
	
df_s = read_key();	
api_key = df_s.api_key[0]
secret_key = df_s.secret_key[0]
passphrase = df_s.passphrase[0]

flag = '1'
tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)
accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
publicAPI = Public.PublicAPI(api_key, secret_key, passphrase, False, flag)
# result = accountAPI.get_position_mode('long_short_mode')
result = accountAPI.get_position_mode('net_mode')

def read_account():
	global flag
	fundingAPI = Funding.FundingAPI(api_key, secret_key, passphrase, False, flag)
	result = fundingAPI.get_balances()
	if result is None:
		return None
	elif len(result['data'])==0:
		print(result)
		return 0
	return(result['data'][-1]['cashBal'])
	
def def_str(mystr):
	min2 = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	inputstr='\n'+min2+','+str(mystr)
	if os.stat(r'str.csv').st_size == 0:
		f=open(r'str.csv','w');f.write(inputstr);f.close()
	else:
		f=open(r'str.csv','a+');f.write(inputstr);f.close()
config_list = ['symbol','open_action','open_cap_rate','open_cap_lever','open_toMA','close_toMA',
				'open_freq','close_freq','open_gap','close_hold','cb_within_without',
				'ma_n_open','ma_n_close','long_limit','stop']

def isnum(s):
    try:
        float(s)
        return True
    except ValueError:
        pass 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass 
    return False
	
def ema_x(df, n):
    EMA = pd.Series(df['close'].ewm(span=n, min_periods=n).mean(), name='ema_' + str(n))
    df = df.join(EMA)
    return df['ema_' + str(n)]
	
def ma_x(df, n):
    # MA = pd.Series(df['close'].rolling(n, min_periods=n).mean(), name='MA_' + str(n))
	MA = pd.Series(df['close'].rolling(window=n).mean(), name='MA_')
	df = df.join(MA)
	df['dis'] = df['close'] - df['MA_']
	def_str('C MA C-MA '+str(df['close'].iloc[-1])+' '+str(df['MA_'].iloc[-1])+' '+str(df['dis'].iloc[-1]))
	return df[['open','high','low','close', 'MA_',  'dis']]

def ma_buy(df, n, limit,exist):
	if exist == 'empty':
		if df['dis'].iloc[-1] >= n and df['low'].iloc[-1] <= df['MA_'].iloc[-1] <= df['close'].iloc[-1] and df['dis'].iloc[-1] - n <= limit:
			return(-10)
		if df['dis'].iloc[-1] >= n and df['low'].iloc[-2] <= df['MA_'].iloc[-2] and df['close'].iloc[-1] >= df['MA_'].iloc[-1] and df['dis'].iloc[-1] - n <= limit:
			return(-10)
	else:
		if df['close'].iloc[-1]-df['MA_'].iloc[-1] >= n:
			return(-10)
	return(0)

def ma_sell(df, n, limit,exist):
	if exist == 'empty':
		if df['dis'].iloc[-1] < 0 and limit > df['MA_'].iloc[-1]-df['close'].iloc[-1] >= n and df['high'].iloc[-1] >= df['MA_'].iloc[-1] >= df['close'].iloc[-1]:
			return(100)
		if df['dis'].iloc[-1] < 0 and limit > df['MA_'].iloc[-1]-df['close'].iloc[-1] >= n and df['high'].iloc[-2] >= df['MA_'].iloc[-2] and df['close'].iloc[-1] <= df['MA_'].iloc[-1]:
			return(100)
	else:
		if df['MA_'].iloc[-1]-df['close'].iloc[-1] >= n:
			return(100)
	return(0)

def ma_buy_without(df, n, limit):
	if limit > df['close'].iloc[-1]-df['MA_'].iloc[-1] >= n:
		return(-10)
	return(0)

def ma_sell_without(df, n, limit):
	if limit > df['MA_'].iloc[-1]-df['close'].iloc[-1] >= n:
		return(100)
	return(0)

def file_name_walk(file_dir):
	for root, dirs, files in os.walk(file_dir):
		len(files)
	return files	
	
def stop_all():
	df_cfg = read_config()
	print(df_cfg)
	if df_cfg is None:
		return
	for i in range(len(list(df_cfg['symbol']))):	
		df = df_cfg[df_cfg['symbol'] == df_cfg['symbol'].iloc[i]]
		# df.loc[0,'stop'] = 'True'
		df.at[0,'stop'] = 'True'
		df.to_csv('config/'+df_cfg['symbol'].iloc[i]+'.csv', index=False, mode='w',columns=config_list)
	print('\n len\t',len(df_cfg), '\t df_cfg \n \t\t\t\t\tStop trading !\n', df_cfg['symbol'])
		
def read_config():
	files = file_name_walk('config/');	df_cfg=pd.DataFrame({})
	if len(files)==0:
		return None

	for i in range(len(files)):
		df = pd.read_csv('config/'+files[i], dtype={'symbol': str, 'open_action': str, 
		'open_cap_rate': float, 'open_cap_lever': int, 'open_toMA': float,'close_toMA': float, 'open_freq': int,
		'close_freq': int, 'open_gap': int,'close_hold': int, 'cb_within_without': str,
		'ma_n_open': int, 'ma_n_close': int,'long_limit': float,'stop': bool}, engine='python')

		df_cfg = df_cfg.append(df)
	# print(df_cfg)
	return(df_cfg)

def get_pos_qty(symbol):
	result = accountAPI.get_positions(instType='SWAP', instId=symbol)
	# print(result)
	df = pd.DataFrame({})
	if result is None:
		def_str('get_pos_qty result is None '+str(result))
		return df
	elif len(result['data'])==0:
		def_str('get_pos_qty len 0 ')
		return df

	print(result['data'][-1]['pos']);print('\n')

	df = pd.DataFrame(result['data'])
	df = df[['instId','margin','avgPx','pos','posSide']]
	df = df.drop(index=df[df['pos']==''].index)
	# print('pos\t',df['pos']);	time.sleep(3)
	print(df)
	
	return(df)
	# return(result['data'][-1]['pos'])

# print(get_pos_qty('BTC-USD-SWAP'))
# print('exit')
# sys.exit()
def get_all_qty(): # limit 10 / 2s
	files = file_name_walk('config/');	# print(files)
	df = pd.DataFrame({})
	if len(files)==0:
		return None
	for i in range(len(files)):
		symbol = files[i].replace('.csv','')
		print(get_pos_qty(symbol))
		df = df.append(get_pos_qty(symbol))
	return(df)

def get_max(symbol):
	accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
	result = accountAPI.get_maximum_trade_size(symbol, 'isolated', leverage='')
	
	if result is None:
		def_str('get_max result is None '+str(result))
		return None
	elif len(result['data'])==0:
		def_str('get_max len 0 ')
		return None
	
	print(result)

	return (min(int(result['data'][-1]['maxBuy']), int(result['data'][-1]['maxSell'])))