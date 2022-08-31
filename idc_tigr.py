import json,sys,csv,time,re,os
import pandas as pd
from datetime import datetime,timedelta
from idc import *
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

def def_str(mystr):
	min2 = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	inputstr='\n'+min2+','+str(mystr)
	if os.stat(r'str.csv').st_size == 0:
		f=open(r'str.csv','w');f.write(inputstr);f.close()
	else:
		f=open(r'str.csv','a+');f.write(inputstr);f.close()



def get_days(cont):
	return((pd.to_datetime(cont, format='%Y-%m-%d')[0] - datetime.today()).days)


	
def def_txt(mystr):
	min2 = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	inputstr='\n'+min2+','+str(mystr)
	if os.stat(r'error.csv').st_size == 0:
		f=open(r'error.csv','w');f.write(inputstr);f.close()
	else:
		f=open(r'error.csv','a+');f.write(inputstr);f.close()
	# 保证金模式 ： isolated 逐仓 ，cross：全仓
	# 非保证金模式 ： cash 非保证金
	#  tgtCcy , base_ccy 交易货币 ; quote_ccy : 计价货币 仅用于币币订单
def place_(symbol, act, posSide, quantity):

	print(symbol, act, posSide, quantity)
	flag = '1'

	tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)

	result = tradeAPI.place_order(instId=symbol, tdMode='isolated', side=act, posSide=posSide,
								   ordType='market', sz=str(quantity),tgtCcy='')
	if result['data'][-1]['ordId'] != '':
		print('\n',result['data'])							   
		# print('\n',result['data'][-1]['sMsg'])
		return (str(result['data'][-1]['ordId'])+result['data'][-1]['sMsg'])
	else:
		print('\n',result['data'])	
		print('下单失败 ',result['data'][-1]['sMsg'])
		def_str('下单失败 '+result['data'][-1]['sMsg'])
		return None

def read_local(symbol):
	pos_path = 'error.csv'
	if os.stat(pos_path).st_size == 0:
		return pd.DataFrame({})
	df_pos = pd.read_csv(pos_path, engine='python', header=None, 
	names=['time_key','symbol','act','quantity','oc'])
	df_pos = df_pos[df_pos['symbol'] == symbol]
	return(df_pos)
	
def read_act(symbol):
	pos_path = 'error.csv'
	if os.stat(pos_path).st_size == 0:
		return pd.DataFrame({})
	try:
		df_pos = pd.read_csv(pos_path, engine='python', header=None, 
		names=['time_key','symbol','act','quantity','oc'])
		df_pos = df_pos[df_pos['symbol'] == symbol]
		return(df_pos[['act','oc']].iloc[-1]['act'], df_pos[['act','oc']].iloc[-1]['oc'])
	except Exception as e:
		def_str('read_act error '+str(e))
		return None

def read_local_last():
	pos_path = 'error.csv'
	df_pos = pd.read_csv(pos_path, engine='python', header=None, 
	names=['time_key','symbol','act','quantity','oc'])
	if len(df_pos)>0:
		return(df_pos.iloc[-1])
	else:
		return(pd.DataFrame({}))
	
def get_minutes(a,b):
	return((pd.to_datetime(a, format='%Y-%m-%d %H:%M:%S')-
	pd.to_datetime(b, format='%Y-%m-%d %H:%M:%S')).seconds/60)
		
def get_now(symbol):
	df_loc = read_local(symbol)
	if len(df_loc)>0:
		try:
			b = df_loc[(df_loc['oc'] == 'open')]['time_key'].iloc[-1]
			return((datetime.now()-
			pd.to_datetime(b, format='%Y-%m-%d %H:%M:%S')).seconds/60)
		except:
			return -1
	return -1



def read_margin2(symbol):
	symbol = re.sub(r'[0-9]+', '', symbol)	
	df = pd.read_csv('margin2.csv')
	df.dropna(inplace=True)

	df = df[df['symbol']==symbol]
	return(df['MT'].iloc[0])
	
def read_mt(symbol):
	symbol = re.sub(r'[0-9]+', '', symbol)
	df = pd.read_csv('margin2.csv')
	df.dropna(inplace=True)

	df = df[df['MT']==symbol]
	return(df[['MT','symbol']])

def match_mt(symbol,MT):
	symbol = re.sub(r'[0-9]+', '', symbol)
	a= (read_margin2(symbol))
	if a['MT'].iloc[0] == MT:
		return True
	return False

# c= (read_mt('GOLD'))
	
# a= (read_margin2('GC'))
# b= (read_margin2('MGC'))

# print(a)
# print(b)

# sys.exit()
	
def read_margin(symbol):	
	df = pd.read_csv('margin.csv')
	df.dropna(inplace=True)
	df['Initial'] = df['Initial'].astype(float)
	sym = re.sub(r'[0-9]+', '', symbol)
	df = df[df['symbol']==sym]
	return(df[['symbol','Initial']])

def get_qty(symbol, rate, cash):
	print(cash, read_margin(symbol)['Initial'].iloc[0], cash * rate)
	def_str(str(cash) +'  '+ str(rate)+'  '+str(read_margin(symbol)['Initial'].iloc[0]))
	return( int(cash * rate / read_margin(symbol)['Initial'].iloc[0]))
	# return((cash * rate) / read_margin(symbol)['Initial'].iloc[0])
# print(get_qty('MNQ2203',0.006,200000))
# sys.exit()
def get_filled(symbol_arg):
	paper = read_account()
	df = pd.DataFrame({})
	orders = trade_client.get_orders(account=paper, sec_type=SecurityType.FUT, market=Market.ALL)
	for i in range(len(orders)):
		if orders[i].filled > 0:
		# if 1>0:
			n = str(orders[i].contract).find('/')
			str_n = str(orders[i].contract)[0:n]
			symbol = str_n;	
			df=df.append({'action':orders[i].action,'symbol':symbol,'contract':str_n,'trade_time':orders[i].trade_time,
			'quantity':orders[i].quantity,'filled':orders[i].filled,
			'avg_fill_price':orders[i].avg_fill_price},ignore_index=True)
			# print(orders[i]['trade_time','action','quantity','filled','avg_fill_price'])
	if len(df)>0:
		df['trade_time']=df['trade_time'].apply(lambda d: datetime.fromtimestamp(int(d)/1000).strftime('%Y-%m-%d %H:%M:%S'))
		df = df[df['symbol'] == symbol_arg]
		print(symbol_arg)
		# df.to_csv('fill.csv', index=False, mode='a',columns=['symbol','trade_time','avg_fill_price'])
		# return(df.iloc[0])
		return(df)
	else:
		return None

def clear_all(symbol):
	df_ret=pd.DataFrame({'symbol':[],'act':[],'quantity':[],'oc':[]});	action='None';	lst=[]

	if symbol == 'all':
		df_sym = read_config()
		lst = list(df_sym['symbol'])
	else:
		lst.append(symbol)
	print(lst)
		
	for i in range(len(lst)):
		df = get_pos_qty(lst[i])
		if len(df) == 0:
			continue
		print(len(df))
		qty = int(df['pos'].iloc[-1])
		print(lst[i],qty)
		
		if qty > 0:
			place_(lst[i],'sell','net',abs(qty));	action='SELL'			
		elif qty < 0:
			place_(lst[i],'buy','net',abs(qty));		action='BUY'	
		if qty!=0:
			df_ret=df_ret.append({'act':action,'symbol':lst[i],'quantity':abs(qty),'oc':'close'},ignore_index=True)

	return(df_ret)
