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
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

if __name__ == '__main__':
	api_key = 'c293d81d-3ae0-4f7b-b4ef-ce07b52522f9'
	secret_key = 'AEAAEDD73050318A464879E85388C665'
	passphrase = "qwer1234"

	flag = '1'  # 模拟盘 demo trading
	# flag = '0'  # 实盘 real trading

	# account api
	# accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)

	# market api
	# symbol = 'BTCUSDT' # not support
	
	symbol = 'BTC-USD-SWAP'
	marketAPI = Market.MarketAPI(api_key, secret_key, passphrase, False, flag)
	
	ticker = marketAPI.get_ticker(symbol)
	print(ticker);print('\n')

	result = marketAPI.get_candlesticks(symbol, bar='1m')
	r_data = result['data']

	df = pd.DataFrame(r_data,columns = ['time_key','open','high','low','close','volume','volumeB'])

	df['time_key']=df['time_key'].apply(lambda d: datetime.fromtimestamp(int(d)/1000).strftime('%Y-%m-%d %H:%M:%S'))

	print(df.head(5))
	print(df.tail(5))
	sys.exit()
	# print(result['data'])
	
	
	# 获取所有产品行情信息  Get Tickers
	# result = marketAPI.get_tickers('SPOT')
	# 获取单个产品行情信息  Get Ticker
	# result = marketAPI.get_ticker('BTC-USDT')
	# 获取指数行情  Get Index Tickers
	# result = marketAPI.get_index_ticker('BTC', 'BTC-USD')
	# 获取产品深度  Get Order Book
	# result = marketAPI.get_orderbook('BTC-USDT-210402', '400')

	# 获取交易产品历史K线数据（仅主流币实盘数据）  Get Candlesticks History（top currencies in real-trading only）
	# result = marketAPI.get_history_candlesticks('BTC-USDT')
	# 获取指数K线数据  Get Index Candlesticks
	# result = marketAPI.get_index_candlesticks('BTC-USDT')
	# 获取标记价格K线数据  Get Mark Price Candlesticks
	# result = marketAPI.get_markprice_candlesticks('BTC-USDT')
	# 获取交易产品公共成交数据  Get Trades
	# result = marketAPI.get_trades('BTC-USDT', '400')
	# 获取平台24小时成交总量  Get Platform 24 Volume
	# result = marketAPI.get_volume()
	# Oracle 上链交易数据 GET Oracle
	# result = marketAPI.get_oracle()
	# 获取指数成分数据 GET Index Components
	# result = marketAPI.get_index_components(index='')
	# 获取法币汇率 GET exchange rate in legal currency
	# result = marketAPI.get_exchange_rate()

	# public api
	publicAPI = Public.PublicAPI(api_key, secret_key, passphrase, False, flag)
	# 获取交易产品基础信息  Get instrument
	# result = publicAPI.get_instruments('FUTURES', 'BTC-USDT')
	# 获取交割和行权记录  Get Delivery/Exercise History
	# result = publicAPI.get_deliver_history('FUTURES', 'BTC-USD')
	# 获取持仓总量  Get Open Interest
	# result = publicAPI.get_open_interest('SWAP')
	# 获取永续合约当前资金费率  Get Funding Rate
	# result = publicAPI.get_funding_rate('BTC-USD-SWAP')
	# 获取永续合约历史资金费率  Get Funding Rate History
	# result = publicAPI.funding_rate_history('BTC-USD-SWAP')
	# 获取限价  Get Limit Price
	# result = publicAPI.get_price_limit('BTC-USD-SWAP')
	# 获取期权定价  Get Option Market Data
	# result = publicAPI.get_opt_summary('BTC-USD')
	# 获取预估交割/行权价格  Get Estimated Delivery/Excercise Price
	# result = publicAPI.get_estimated_price('ETH-USD-210326')
	# 获取免息额度和币种折算率  Get Discount Rate And Interest-Free Quota
	# result = publicAPI.discount_interest_free_quota('')
	# 获取系统时间  Get System Time
	# result = publicAPI.get_system_time()
	# 获取平台公共爆仓单信息  Get Liquidation Orders
	# result = publicAPI.get_liquidation_orders('FUTURES', uly='BTC-USDT', alias='next_quarter', state='filled')
	# 获取标记价格  Get Mark Price
	# result = publicAPI.get_mark_price('FUTURES')
	# 获取合约衍生品仓位档位 Get Position Tiers
	# result = publicAPI.get_tier(instType='MARGIN', instId='BTC-USDT', tdMode='cross')
	# 获取杠杆利率和借币限额公共信息 Get Interest Rate and Loan Quota
	# result = publicAPI.get_interest_loan()
	# 获取合约衍生品标的指数 Get underlying
	# result = publicAPI.get_underlying(instType='FUTURES')
	# 获取尊享借币杠杆利率和借币限额 GET Obtain the privileged currency borrowing leverage rate and currency borrowing limit
	# result = publicAPI.get_vip_interest_rate_loan_quota()

	# trading data
	tradingDataAPI = TradingData.TradingDataAPI(api_key, secret_key, passphrase, False, flag)
	# 获取支持币种 Get support coin
	# result = tradingDataAPI.get_support_coin()
	# 获取币币或衍生品主动买入/卖出情况 Get taker volume
	# result = tradingDataAPI.get_taker_volume(ccy='BTC', instType='SPOT')
	# 获取杠杆多空比 Get Margin lending ratio
	# result = tradingDataAPI.get_margin_lending_ratio('BTC')
	# 获取多空持仓人数比 Get Long/Short ratio
	# result = tradingDataAPI.get_long_short_ratio('BTC')
	# 获取持仓总量及交易量 Get contracts open interest and volume
	# result = tradingDataAPI.get_contracts_interest_volume('BTC')
	# 获取期权合约持仓总量及交易量 Get Options open interest and volume
	# result = tradingDataAPI.get_options_interest_volume('BTC')
	# 看涨/看跌期权合约 持仓总量比/交易总量比 Get Put/Call ratio
	# result = tradingDataAPI.get_put_call_ratio('BTC')
	# 看涨看跌持仓总量及交易总量（按到期日分） Get open interest and volume (expiry)
	# result = tradingDataAPI.get_interest_volume_expiry('BTC')
	# 看涨看跌持仓总量及交易总量（按执行价格分）Get open interest and volume (strike)
	# result = tradingDataAPI.get_interest_volume_strike('BTC', '20210924')
	# 看跌/看涨期权合约 主动买入/卖出量  Get Taker flow
	# result = tradingDataAPI.get_taker_flow('BTC')

	# trade api
	tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)
	# 下单  Place Order
	# result = tradeAPI.place_order(instId='BTC-USDT-210326', tdMode='cross', side='sell', posSide='short',
	#							   ordType='market', sz='100',tgtCcy='')
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
