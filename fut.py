import okx.Account_api as Account
import okx.Funding_api as Funding
import okx.Market_api as Market
import okx.Public_api as Public
import okx.Trade_api as Trade
import okx.status_api as Status
import okx.subAccount_api as SubAccount
import okx.TradingData_api as TradingData				# BTC-USD-SWAP
import okx.Broker_api as Broker
import json,sys,csv,time,threading
import pandas as pd
from idc_tigr import *
import numpy as np
from datetime import datetime,timedelta
from idc import *

pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 1000)

df_mt = pd.DataFrame({});	signal = ''; df_ps = {};	k=0;	mt_path = '';	od_date=[]

min2 = (datetime.now().strftime('%Y-%m-%d %H:%M')+':00')

os.environ["http_proxy"] = "http://127.0.0.1:10809"
os.environ["https_proxy"] = "http://127.0.0.1:10809"
df_s = read_key();	
api_key = df_s.api_key[0]
secret_key = df_s.secret_key[0]
passphrase = df_s.passphrase[0]

print('\nGet setting key.csv\n',api_key,secret_key,passphrase)

print('SIMULATE',read_account())

# print('REAL')
# read_account('0')
ok_path = 'okex.csv'
df_ok = pd.read_csv(ok_path, engine='python',dtype=str)
list_ok = list(df_ok['symbol'])
print(list_ok)

def get_mt(): # need to renew
	global mt_path
	pathd = r'C:\Program Files\MetaTrader 5 EXNESS\MQL5\Files\76027123_交易数据1.csv'
	# pathd = r'C:\Program Files\MetaTrader 5 EXNESS\MQL5\Files\bk.csv'
	
	mt_path = pathd
# XAUUSD,SELL,CLOSE,2022.03.02 12:51:53,2022.03.02 20:51:53,2906966
# BTCUSD,SELL,CLOSE,2022.03.02 12:51:52,2022.03.02 20:51:52,2906964
	# try:
	if True:
		# pathd = r'C:\MT5交易数据中转'
		print('\t\t\t\t\t\t',pathd)
		df = pd.read_csv(pathd, engine='python', names = ['MT','action','oc','timeEU','timeBJ','ID'])
		return(df)

	return None

def get_kline( symbol, K_type_A, K_type_B, dis_open, dis_close, cb_with, ma_n_open, ma_n_close, 
open_gap, close_hold, open_action, open_qty, open_cap_lever, long_limit):
	global signal, df_s, df_ps, k, df_mt
	min3 = datetime.now().strftime('%H:%M:%S')
	print(ma_n_open,ma_n_close, '\t\t', min3)
	qty = int(open_qty);	signal='?';		df=pd.DataFrame({});		action = 'EMP'
	if qty==0:
		def_str(' qty 0')
		return None
		
	# print('\nget_all_qty')
	# df_all = get_all_qty()
	
	# if len(df_all) == 0:
		# exist = 'empty'
	
	df = get_pos_qty(symbol);	
	print('\t\t\t\t\t  Start get Pos len df',len(df))

	print(len(df))
	if len(df) == 0:
		exist = 'empty'
		dis = dis_open;	
	else:
		if float(df['pos'][0]) > 0:
			exist = 'long'
		elif float(df['pos'][0]) < 0:
			exist ='short'
		else:
			exist = 'empty'
		dis = dis_close;
		def_str(str(df))

	if exist == 'empty':
		oc = 'OPEN'
	else:
		oc = 'CLOSE'
		
	print('\n',symbol,exist);		def_str(symbol +' '+ exist)

	if len(df_mt) == 0:
		print('len df_mt 0 return');return None
	
	if(open_gap > 0 and close_hold > 0) :
		open_till = get_now(symbol)
		def_str(symbol+'  '+'open_till '+str(round(open_till,1)))
		if open_till != -1 and open_till < open_gap and exist == 'empty':
			signal = 'open_gap cancel';		print('\t\t\t\t\t', round(open_till,1),open_gap,signal);	return None
		elif open_till != -1 and open_till < close_hold and exist != 'empty':
			signal = 'close_hold cancel';	print('\t\t\t\t\t', round(open_till,1),close_hold,signal);	return None

	# code_mt = 'BTCUSD'
	
	print(symbol in list(df_ok['symbol']))
	df_tmp = df_ok[df_ok['symbol'] == symbol]
	code_mt = df_tmp['backup'].iloc[0]
	
	# print(df_mt, code_mt, df_mt['MT'])
	df_1 = df_mt[df_mt['MT'] == code_mt]
	
	print(df_1[['MT','action','oc']], '\n \t Direction same ? \n')
	
	print('持仓操作方向', 'MT方向', 'MT指令')
	if len(df_1) == 0:
		print(symbol+' MT 0')
		def_str(symbol+' MT 0')
		return
	def_str(str(df_1))
	print(oc,'\t', df_1['oc'].iloc[0],'\t',  df_1['action'].iloc[0])
	action = df_1['action'].iloc[0]

	print('指令 买', '指令 卖')
	print(action == 'BUY', '\t', action == 'SELL')	

	posSide = action.lower()
	if action == 'SELL' and exist=='empty':
		posSide = posSide.replace('sell','net')
	elif action == 'SELL' and exist=='long':
		posSide = posSide.replace('sell','net')
	
	if action == 'BUY' and exist=='empty':
		posSide = posSide.replace('buy','net')
	elif action == 'BUY' and exist=='short':
		posSide = posSide.replace('buy','net')	
	posSide = 'net'
	print('ready to order', symbol,posSide, qty, '\n')
	
	order_bool = False
	def_str(exist + open_action + action)
	print(exist + open_action + action + symbol)
	
	if df_1['timeBJ'].iloc[0] in od_date:
		def_str('timeBJ cancel')
		print('timeBJ cancel')
		return
		
	od_date.append(df_1['timeBJ'].iloc[0])
	
	time.sleep(10)
	if (exist=='empty' and open_action!='SHORT') or exist=='short':
		if action == 'BUY':
			print('指令 买', ' 准备下单');	order_bool = True
			od_str = place_(symbol,'buy',posSide,qty);print(symbol,'buy',posSide,qty,od_str);time.sleep(3)
			def_str('MT test BUY '+str(od_str))
			if od_str is None:
				return
			
	if ((exist=='empty' and open_action!='LONG') or exist=='long'):
		if action == 'SELL':
			print('指令 卖', ' 准备下单');	order_bool = True
			od_str = place_(symbol,'sell',posSide,qty);print(symbol,'sell',posSide,qty,od_str);time.sleep(3)
			def_str('MT test SELL '+str(od_str))
			if od_str is None:
				return
				
	if order_bool == True:
		print('\t\t\t get_mt size ',os.stat(mt_path).st_size)
		f=open(mt_path,'w');f.write('');f.close()
		print('\t\t\t get_mt size ',os.stat(mt_path).st_size)
		df_mt = get_mt()
	
		print('下单成功')
		def_txt(symbol+','+action+','+str(qty)+','+oc)
		return([symbol,action,qty,oc])
	else:
		print('下单条件未满足 order_bool == False')

def t2():

	global df_cfg,df_ps,cash,k,mt_path,df_mt
	
	while 1:
		k += 1
		wk=datetime.today().weekday()

		if int(str(datetime.now())[17:19]) % 2 == 0:
			df_mt = get_mt()
			if df_mt is None or len(df_mt)==0:
				time.sleep(0.5)
				print('\t\t\t\t\t Failed to read mt data')
				time.sleep(0.5)
				# continue
			else:
				def_str('read mt data')
			
			df_cfg = read_config()
			# df_ps = get_pos()
			# cash = get_cash()
			print('\t\t\t get_mt size ',os.stat(mt_path).st_size, len(df_cfg))
			if len(df_cfg) > 0 : 
				for i in range(len(df_cfg)):
					# if df_cfg['stop'].iloc[i] == True:
						# print(df_cfg['symbol'].iloc[i], '\t stop');	continue
					if float(df_cfg['open_cap_rate'].iloc[i]) == 1:
						open_qty = 1
					else:
					
						# open_qty = get_qty(df_cfg['symbol'].iloc[i], float(df_cfg['open_cap_rate'].iloc[i])/100, cash)
						# print('open_qty\t ',open_qty)
						
						max_trade = get_max(df_cfg['symbol'].iloc[i])					
						open_qty = int(int(df_cfg['open_cap_rate'].iloc[i]) / 100 * max_trade)
						print(open_qty)
						
						if open_qty <=0:
							def_str(df_cfg['symbol'].iloc[i]+' get_qty error');		time.sleep(0.5)
							continue

					time.sleep(0.5)

					if 1>0:
						trade_ret = get_kline(df_cfg['symbol'].iloc[i],df_cfg['open_freq'].iloc[i], 
									df_cfg['close_freq'].iloc[i], df_cfg['open_toMA'].iloc[i], 
									df_cfg['close_toMA'].iloc[i], df_cfg['cb_within_without'].iloc[i],
									int(df_cfg['ma_n_open'].iloc[i]), int(df_cfg['ma_n_close'].iloc[i]),
									df_cfg['open_gap'].iloc[i], df_cfg['close_hold'].iloc[i], 
									df_cfg['open_action'].iloc[i], open_qty, df_cfg['open_cap_lever'].iloc[i],
									float(df_cfg['long_limit'].iloc[i]))

					time.sleep(0.5)
		time.sleep(0.5)

if __name__ == '__main__':
	f=open(r'str.csv','w');f.write('');f.close()
	f=open(r'error.csv','w');f.write('');f.close()
	print('clear str.csv')
	
	print(clear_all('all'))
	t2()

	sys.exit()