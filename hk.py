from futu import *
from datetime import datetime,timedelta
import os,os.path,time,sys,csv,re
import json
import pandas as pd
def def_txt(mystr):
	min2 = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	inputstr='\n'+min2+','+str(mystr)
	f=open(r'error.csv','a+');f.write(inputstr);f.close()
	
quote_ctx = OpenQuoteContext(host='42.193.124.183', port=11111)
list = ['HK.800000']
ret_sub, err = quote_ctx.subscribe(list, [SubType.K_1M], subscribe_push=False)
if ret_sub == RET_OK:
	ret, data_9 = quote_ctx.get_cur_kline(list[0], 15, SubType.K_1M)
	print(data_9['close'])
else:
	print(err)

quote_ctx.close()
sys.exit()
	
def read_margin():	
	df = pd.read_csv('margin.csv')
	df.dropna(inplace=True)
	df['Initial'] = df['Initial'].astype(float)
	
	for i in range(len(df)):
	
		df.at[i,['symbol']] = 'US.'+re.sub(r'[0-9]+', '', df['symbol'].iloc[i])+'main'
	
	# df = df[~df['名字'].str.contains('ST')]
	df = df[df['symbol'].str.contains('US.')]
	
	df_fut=[]
	
	print(len(df))

	return(df['symbol'])

df_fut = read_margin()

print(len(df_fut))
print(df_fut)
fut_list = list(df_fut)
fut_list.remove('US.MKmain')

fut_list=[]
fut_list.append('US.VXmain')
fut_list.append('US.RTYmain')
fut_list.append('US.CLmain')
fut_list.append('US.GCmain')
fut_list.append('US.NGmain')
fut_list.append('HK.MHImain')
fut_list.append('US.ESmain')
fut_list.append('US.YMmain')
fut_list.append('US.NQmain')
fut_list.append('US.6Emain')
fut_list.append('US.6Bmain')
fut_list.append('US.6Amain')

print(fut_list,type(fut_list))
if __name__ == '__main__':
#_OPEN 
	quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

	# ret, data = quote_ctx.get_market_state(fut_list)
	
	while True:

		ret, data = quote_ctx.get_market_state(fut_list)
		if ret == RET_OK:
			print(data)
			# def_txt(str(data['code'].iloc[0]+' '+str(data['market_state'].iloc[0])))
			data.to_csv('error.csv', index=False, mode='a', columns=['code','market_state'])
			def_txt('sleep 5')
		else:
			print('error:', data)
		time.sleep(5)
			
	quote_ctx.close()
	sys.exit()

