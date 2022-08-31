import json,os,sys
from datetime import datetime
import pandas as pd
import numpy as np
import okx.Account_api as Account
import okx.Funding_api as Funding
import okx.Market_api as Market
import okx.Public_api as Public
import okx.Trade_api as Trade
import okx.status_api as Status
import okx.subAccount_api as SubAccount
import okx.TradingData_api as TradingData				# BTC-USD-SWAP
import okx.Broker_api as Broker
os.environ["http_proxy"] = "http://127.0.0.1:108099"
os.environ["https_proxy"] = "http://127.0.0.1:108099" #print(os.system("ping www.google.com"))

if __name__ == '__main__':
	api_key = 'c293d81d-3ae0-4f7b-b4ef-ce07b52522f9'
	secret_key = 'AEAAEDD73050318A464879E85388C665'
	passphrase = "qwer1234"

	flag = '1'  # 模拟盘 demo trading
	# flag = '1'  # 实盘 real trading

	symbol = 'BTC-USD-SWAP'

	# public api
	publicAPI = Public.PublicAPI(api_key, secret_key, passphrase, False, flag)
	# 获取交易产品基础信息  Get instrument
	result = publicAPI.get_instruments('FUTURES', symbol)
	print(result['data'][-1])
	

	# trading data
	tradingDataAPI = TradingData.TradingDataAPI(api_key, secret_key, passphrase, False, flag)

	result = tradingDataAPI.get_support_coin()
	print(result,'\n\n')
	print(result['data']['spot'])
	
	symbols = result['data']['spot']

	# for symbol in symbols:

	# trade api
	tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)

	# 保证金模式 ： isolated 逐仓 ，cross：全仓
	# 非保证金模式 ： cash 非保证金
	#  tgtCcy , base_ccy 交易货币 ; quote_ccy : 计价货币 仅用于币币订单
	result = tradeAPI.place_order(instId='BTC-USD-SWAP', tdMode='cross', side='sell', posSide='short',
								   ordType='market', sz='100',tgtCcy='')
	
	
	
	# 批量下单  Place Multiple Orders
	# result = tradeAPI.place_multiple_orders([
	#	 {'instId': 'BTC-USD-SWAP', 'tdMode': 'isolated', 'side': 'buy', 'ordType': 'limit', 'sz': '1', 'px': '17400',
	#	  'posSide': 'long',
	#	  'clOrdId': 'a12344', 'tag': 'test1210','tgtCcy':''},
	#	 {'instId': 'BTC-USD-210409', 'tdMode': 'isolated', 'side': 'buy', 'ordType': 'limit', 'sz': '1', 'px': '17359',
	#	  'posSide': 'long',
	#	  'clOrdId': 'a12344444', 'tag': 'test1211','tgtCcy':''}
	# ])

	# 撤单  Cancel Order
	# result = tradeAPI.cancel_order('BTC-USD-201225', '257164323454332928')
	# 批量撤单  Cancel Multiple Orders
	# result = tradeAPI.cancel_multiple_orders([
	#	 {"instId": "BTC-USD-SWAP", "ordId": "297389358169071616"},
	#	 {"instId": "BTC-USD-210409", "ordId": "297389358169071617"}
	# ])

	# 修改订单  Amend Order
	# result = tradeAPI.amend_order()
	# 批量修改订单  Amend Multiple Orders
	# result = tradeAPI.amend_multiple_orders(
	#	 [{'instId': 'BTC-USD-201225', 'cxlOnFail': 'false', 'ordId': '257551616434384896', 'newPx': '17880'},
	#	  {'instId': 'BTC-USD-201225', 'cxlOnFail': 'false', 'ordId': '257551616652488704', 'newPx': '17882'}
	#	  ])

	# 市价仓位全平  Close Positions
	# result = tradeAPI.close_positions('BTC-USDT-210409', 'isolated', 'long', '')
	# 获取订单信息  Get Order Details
	# result = tradeAPI.get_orders('BTC-USD-201225', '257173039968825345')
	# 获取未成交订单列表  Get Order List
	# result = tradeAPI.get_order_list()
	# 获取历史订单记录（近七天） Get Order History (last 7 days）
	# result = tradeAPI.get_orders_history('FUTURES')
	# 获取历史订单记录（近三个月） Get Order History (last 3 months)
	# result = tradeAPI.orders_history_archive('FUTURES')
	# 获取成交明细(三天)  Get Transaction Details
	# result = tradeAPI.get_fills
	# 获取成交明细(三个月)  Get Transaction Details History
	# result = tradeAPI.get_fills_history(instType='SPOT')
	# 策略委托下单  Place Algo Order
	result = tradeAPI.place_algo_order('BTC-USD-SWAP', 'isolated', 'buy', ordType='conditional',
									   sz='100',posSide='long', tpTriggerPx='60000', tpOrdPx='59999',
									  tpTriggerPxType = 'last', slTriggerPxType = 'last')
	# 撤销策略委托订单  Cancel Algo Order
	# result = tradeAPI.cancel_algo_order([{'algoId': '297394002194735104', 'instId': 'BTC-USDT-210409'}])
	# 撤销高级策略委托订单
	# result = tradeAPI.cancel_advance_algos([ {"algoId":"198273485","instId":"BTC-USDT"}])
	# 获取未完成策略委托单列表  Get Algo Order List
	# result = tradeAPI.order_algos_list('conditional', instType='FUTURES')
	# 获取历史策略委托单列表  Get Algo Order History
	# result = tradeAPI.order_algos_history('conditional', 'canceled', instType='FUTURES')

	# 子账户API subAccount
	subAccountAPI = SubAccount.SubAccountAPI(api_key, secret_key, passphrase, False, flag)
	# 查询子账户的交易账户余额(适用于母账户) Query detailed balance info of Trading Account of a sub-account via the master account
	# result = subAccountAPI.balances(subAcct='')
	# 查询子账户转账记录(仅适用于母账户) History of sub-account transfer(applies to master accounts only)
	# result = subAccountAPI.bills()
	# 删除子账户APIKey(仅适用于母账户) Delete the APIkey of sub-accounts (applies to master accounts only)
	# result = subAccountAPI.delete(pwd='', subAcct='', apiKey='')
	# 重置子账户的APIKey(仅适用于母账户) Reset the APIkey of a sub-account(applies to master accounts only)
	# result = subAccountAPI.reset(pwd='', subAcct='', label='', apiKey='', perm='')
	# 创建子账户的APIKey(仅适用于母账户) Create an APIkey for a sub-account(applies to master accounts only)
	# result = subAccountAPI.create(pwd='', subAcct='', label='trade1', Passphrase='')
	# 查询子账户的APIKey(仅适用于母账户) Create an APIkey for a sub-account(applies to master accounts only)
	# result = subAccountAPI.watch()
	# 查看子账户列表(仅适用于母账户) View sub-account list(applies to master accounts only)
	# result = subAccountAPI.view_list()
	# 子账户间划转 Transfer between subAccounts
	# result = subAccountAPI.subAccount_transfer(ccy='USDT', amt='1', froms='6', to='6', fromSubAccount='1',
	#											toSubAccount='2')

	# BrokerAPI
	BrokerAPI = Broker.BrokerAPI(api_key, secret_key, passphrase, False, flag)
	# 获取独立经纪商账户信息 GET Obtain independent broker account information
	# result = BrokerAPI.broker_info()
	# 创建子账户 Create sub account
	# result = BrokerAPI.create_subaccount(pwd = '123456', subAcct = 'qwerty', label = '', acctLv = '1')
	# 删除子账户 Delete sub account
	# result = BrokerAPI.delete_subaccount(pwd = '123456', subAcct = 'qwerty')
	# 获取子账户列表 Get sub account list
	# result = BrokerAPI.subaccount_info(page = '', subAcct = '', limit = '')
	# 设置子账户的账户等级 Set account level of sub account
	# result = BrokerAPI.set_subaccount_level(subAcct = 'qwerty', acctLv = '1')
	# 设置子账户的交易手续费费率 Set transaction fee rate of sub account
	# result = BrokerAPI.set_subaccount_fee_rate(subAcct = 'qwerty', instType = 'SPOT', chgType = 'absolute', chgTaker = '0.1bp', chgMaker = '', effDate = '')
	# 创建子账户充值地址 Create sub account recharge address
	# result = BrokerAPI.subaccount_deposit_address(subAcct = 'qwerty', ccy = 'BTC', chain = '', addrType = '', to = '')
	# 获取子账户获取充值记录 Get sub account recharge record
	# result = BrokerAPI.subaccount_deposit_history(subAcct = 'qwerty', ccy = 'BTC', txId = '', state = '', after = '', before = '', limit = '')
	# 获取子账户返佣记录 Get rebate record of sub account
	# result = BrokerAPI.rebate_daily(subAcct = 'qwerty', begin = '', end = '', page = '', limit = '')


	# 系统状态API(仅适用于实盘) system status
	Status = Status.StatusAPI(api_key, secret_key, passphrase, False, flag)
	# 查看系统的升级状态
	# result = Status.status()
	print(json.dumps(result))
