from futu import *
from datetime import datetime,timedelta
from PyQt5.QtCore import QThread ,  pyqtSignal,  QDateTime , QObject,Qt,QRegExp
from PyQt5.QtWidgets import QButtonGroup,QPushButton,QApplication, QLineEdit,QGridLayout,QWidget,QCheckBox,QLabel,QListWidget,QRadioButton
from PyQt5.QtGui import QRegExpValidator
import os,os.path,time,sys,csv,json
from idc_tigr import *
from idc import *

df_s = read_key();	
api_key = df_s.api_key[0]
secret_key = df_s.secret_key[0]
passphrase = df_s.passphrase[0]

flag = '1'

k=-1;	symbols=[];		start_list=[]; 		stop_list=[];	
ospath = os.path.abspath(os.path.dirname(__file__))
wk=datetime.today().weekday();min2=datetime.now().strftime('%Y-%m-%d %H:%M')+':00'
df_total = pd.DataFrame({});	df_cfg = pd.DataFrame({});		df_one = pd.DataFrame({})
config_df = ['symbol','open_action','open_cap_rate','open_cap_lever','open_toMA','close_toMA',
				'open_freq','close_freq','open_gap','close_hold','cb_within_without',
				'ma_n_open','ma_n_close','long_limit','stop']
ok_path = 'okex.csv'
df_ok = pd.read_csv(ok_path, engine='python',dtype=str)
list_ok = list(df_ok['symbol'])
print(list_ok)

class BackendThread(QObject):
	update_date = pyqtSignal(str)
	def run(self):
		while True:
			data = QDateTime.currentDateTime()
			currTime = data.toString("yyyy-MM-dd hh:mm:ss")
			self.update_date.emit( str(currTime) )
			time.sleep(1)

class Window(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		global k
		grid = QGridLayout();
		self.symbol_list=QListWidget(self);
		self.Label_set0=QLabel('币 代码',self);			
		self.symbol=QLineEdit(self);
		self.Label_set1=QLabel('开仓方向设定',self);		self.cb_Both=QCheckBox("多空双开",self);
		self.cb_LONG=QCheckBox("只做多  ",self);			self.cb_SHORT=QCheckBox("只做空  ",self);		
		self.Label_set2=QLabel('资金比例%/杠杆',self);		self.open_cap_rate=QLineEdit('1',self);		
		self.Label_set3=QLabel('开/平仓距离MA',self);		self.open_cap_lever=QLineEdit('10',self);	
		self.open_toMA=QLineEdit('0.09',self);				self.close_toMA=QLineEdit('0.09',self);
		self.Label_set4=QLabel('多/空距离MA限制',self);			
		self.long_limit=QLineEdit('0.1',self);				#self.short_limit=QLineEdit('0.1',self);
		self.Label_set5=QLabel('开仓时间周期',self);			
		self.open_freq=QLineEdit('1',self);		
		self.Label_set6=QLabel('平仓时间周期',self);	
		self.close_freq=QLineEdit('1',self);		
		self.Label_set7=QLabel('开仓间隔时间',self);
		self.open_gap=QLineEdit('0',self);		
		self.Label_set8=QLabel('平仓持仓时间',self);
		self.close_hold=QLineEdit('0',self);		
		self.Label_set9=QLabel('开仓策略设定',self);		
		self.cb_within=QCheckBox("回踩  ",self);			self.cb_without=QCheckBox("不回踩  ",self);		
		self.Label_set10=QLabel('开仓/平仓均线周期',self); 	self.ma_n_open=QLineEdit('10',self);		
		self.Trd=QCheckBox("真实交易",self);				self.ma_n_close=QLineEdit('8',self);	
		self.start_btn=QPushButton('单个开始');				self.stop_btn=QPushButton('单个停止');
		self.close_btn=QPushButton('单个平仓')
		self.cb1_btn=QPushButton('&Q 全部停止');
		self.G_btn3=QPushButton('&G 删除全部配置');		self.R_btn3=QPushButton('&R 保存')
		self.G_btn2=QPushButton('&H 全部平仓');			self.R_btn2=QPushButton('&T 清除')
		self.G_btn1=QPushButton('&J 到期日');		self.R_btn1=QPushButton('&Y 全部开始')
		self.load_btn=QPushButton('查询配置');
		# self.G_btn3.setStyleSheet("background-color:lightgreen;")	;self.R_btn3.setStyleSheet("background-color:orange;")
		# self.G_btn3.setDefault(True)
		grid.addWidget(self.load_btn, 18, 4, 1, 1);
		grid.addWidget(self.G_btn3, 17, 4, 1, 1);	grid.addWidget(self.R_btn3, 15, 4, 1, 1);
		grid.addWidget(self.G_btn2, 17, 6, 1, 1);	grid.addWidget(self.R_btn2, 16, 4, 1, 1);
		grid.addWidget(self.G_btn1, 19, 4, 1, 1);	grid.addWidget(self.R_btn1, 15, 6, 1, 1);
		grid.addWidget(self.start_btn, 15, 5, 1, 1);grid.addWidget(self.cb1_btn, 16, 6, 1, 1);
		grid.addWidget(self.stop_btn, 16, 5, 1, 1); grid.addWidget(self.close_btn, 17, 5, 1, 1);
		self.cb1_btn.clicked.connect(lambda :self.whichbtn(self.cb1_btn))
		self.G_btn3.clicked.connect(lambda :self.whichbtn(self.G_btn3));self.R_btn3.clicked.connect(lambda :self.whichbtn(self.R_btn3))
		self.G_btn2.clicked.connect(lambda :self.whichbtn(self.G_btn2));self.R_btn2.clicked.connect(lambda :self.whichbtn(self.R_btn2))
		self.G_btn1.clicked.connect(lambda :self.whichbtn(self.G_btn1));self.R_btn1.clicked.connect(lambda :self.whichbtn(self.R_btn1))	
		self.start_btn.clicked.connect(lambda :self.whichbtn(self.start_btn));self.stop_btn.clicked.connect(lambda :self.whichbtn(self.stop_btn))	
		self.close_btn.clicked.connect(lambda :self.whichbtn(self.close_btn));self.load_btn.clicked.connect(lambda :self.whichbtn(self.load_btn))	

		self.config_list=QListWidget(self);

		grid.addWidget(self.Label_set0,4,4,1,1);	grid.addWidget(self.symbol,4,5,1,1);			grid.addWidget(self.cb_Both,4,6,1,1);
		grid.addWidget(self.Label_set1,5,4,1,1);	grid.addWidget(self.cb_LONG,5,5,1,1);			grid.addWidget(self.cb_SHORT,5,6,1,1);
		grid.addWidget(self.Label_set2,6,4,1,1);	grid.addWidget(self.open_cap_rate, 6,5,1,1);	grid.addWidget(self.open_cap_lever, 6,6,1,1);	
		grid.addWidget(self.Label_set3,7,4,1,1);	grid.addWidget(self.open_toMA,7,5,1,1);			grid.addWidget(self.close_toMA,7,6,1,1);
		grid.addWidget(self.Label_set4,8,4,1,1);	grid.addWidget(self.long_limit,8,5,1,1);	#grid.addWidget(self.short_limit,8,6,1,1);
		grid.addWidget(self.Label_set5,9,4,1,1);	grid.addWidget(self.open_freq,9,5,1,1);
		grid.addWidget(self.Label_set6,10,4,1,1);	grid.addWidget(self.close_freq,10,5,1,1);
		grid.addWidget(self.Label_set7,11,4,1,1);	grid.addWidget(self.open_gap,11,5,1,1);
		grid.addWidget(self.Label_set8,12,4,1,1);	grid.addWidget(self.close_hold,12,5,1,1);
		grid.addWidget(self.Label_set9,13,4,1,1);	grid.addWidget(self.cb_within,13,5,1,1); grid.addWidget(self.cb_without,13,6,1,1);
		grid.addWidget(self.Label_set10,14,4,1,1);	grid.addWidget(self.ma_n_open,14,5,1,1); grid.addWidget(self.ma_n_close,14,6,1,1);

########
		self.setWindowTitle('Client');
		self.trade_list=QListWidget(self);			self.lb_Acc=QLabel("Account",self)

		self.cb1=QCheckBox("清理",self);			self.lb_Time=QLabel("time",self)
		# grid.addWidget(self.cb_LONG, 31,4,1,1);		grid.addWidget(self.cb_SHORT, 31,5,1,1);
		grid.addWidget(self.trade_list,4,0,11,4);	grid.addWidget(self.lb_Acc, 33, 4, 1, 4);		
		grid.addWidget(self.symbol_list,15,0,3,4);				
		grid.addWidget(self.config_list,18,0,8,4);
		#(1, 0, 1, 2)    第1行,第0列,占用1行,占用2列
		grid.addWidget(self.lb_Time, 33, 0, 1, 1);grid.addWidget(self.cb1, 33, 1, 1, 1);	
		grid.addWidget(self.Trd, 33, 3, 1, 1);		

		self.setLayout(grid);self.resize(500, 580)
		self.G_btn3.hide()

		self.setWindowTitle('OKEX 币交易程式 (WX 1013001850)');
		self.cb_within.setChecked(True)
		self.cb_Both.setChecked(True)
		self.initUI()
		
	def whichbtn(self,btn):
		global trade_list, df_total, symbols, k, df_cfg, start_list, stop_list

		if btn.text() == '查询配置':
			if self.symbol_list.currentItem() is None:
				def_str('currentItem None return')
				self.config_list.addItems(['错误：未选取代码']);return
			df_cfg = read_config()
			if df_cfg is None:
				def_str('df_cfg None return');return
			print('\n len\t',len(df_cfg), '\t df_cfg \n Load settings !\n')
			
			df = df_cfg[df_cfg['symbol']==self.symbol_list.currentItem().text()]
			
			self.symbol.setText(df['symbol'][0])

			if df['open_action'][0] == 'LONG':
				self.cb_LONG.setChecked(True);self.cb_SHORT.setChecked(False);self.cb_Both.setChecked(False)
			elif df['open_action'][0] == 'SHORT':
				self.cb_SHORT.setChecked(True);self.cb_LONG.setChecked(False);self.cb_Both.setChecked(False)
			elif df['open_action'][0] == 'Both':
				self.cb_Both.setChecked(True);self.cb_LONG.setChecked(False);self.cb_SHORT.setChecked(False)

			if df['cb_within_without'][0] == 'within':
				self.cb_within.setChecked(True);self.cb_without.setChecked(False)
			elif df['cb_within_without'][0] == 'without':
				self.cb_without.setChecked(True);self.cb_within.setChecked(False)
				
			self.open_cap_rate.setText(str(df['open_cap_rate'][0]))
			self.open_cap_lever.setText(str(df['open_cap_lever'][0]))
			self.open_toMA.setText(str(df['open_toMA'][0]))
			self.close_toMA.setText(str(df['close_toMA'][0]))
			self.long_limit.setText(str(df['long_limit'][0]))
			# self.short_limit.setText(str(df['short_limit'][0]))
			self.open_freq.setText(str(df['open_freq'][0]))
			self.close_freq.setText(str(df['close_freq'][0]))
			self.open_gap.setText(str(df['open_gap'][0]))
			self.close_hold.setText(str(df['close_hold'][0]))
			self.ma_n_open.setText(str(df['ma_n_open'][0]))	
			self.ma_n_close.setText(str(df['ma_n_close'][0]));

			self.config_list.addItems([df['symbol'][0] + '  查询配置'])
			
			print(get_max(self.symbol.text()))

		elif btn.text() == '&J 到期日' :
			if self.symbol_list.currentItem() is None:
				print('None return')
				self.config_list.addItems(['错误：未选取代码']);return

			a,b = get_remain(self.symbol_list.currentItem().text())
			self.config_list.addItems([a + '  剩余 '+b])
			
		elif btn.text() == '&T 清除':
			if self.symbol_list.currentItem() is None:
				print('None return')
			value = self.symbol_list.currentItem().text()+'.csv'
			sym = self.symbol_list.currentItem().text()
			print("delete file : " + str(value))
			os.remove('config/'+value)
			
			self.symbol_list.clear()
			symbols = file_name_walk('config/')
			if len(symbols)>0:
				for i in range(len(symbols)):
					symbols[i] = symbols[i].replace('.csv','')			
					self.symbol_list.addItems([symbols[i]])
					
			self.config_list.addItems([sym + '  清除'])
			
		elif btn.text() == '&G 删除全部配置':
			del_list = os.listdir('config/')
			for f in del_list:
				file_path = os.path.join('config/', f)
				if os.path.isfile(file_path):
					os.remove(file_path)
			self.config_list.addItems(['删除全部配置'])	
#######
		elif btn.text()=='&R 保存':
			if self.symbol_list.currentItem() is None:
				print('None return')
				self.config_list.addItems(['错误：未选取代码']);return
			open_action=''; with_str=''
			if self.cb_LONG.isChecked():
				open_action = 'LONG'
			elif self.cb_SHORT.isChecked():
				open_action = 'SHORT'
			elif self.cb_Both.isChecked():
				open_action = 'Both'

			if self.cb_within.isChecked():
				with_str = 'within'
			elif self.cb_without.isChecked():
				with_str = 'without'
			if self.symbol.text() == '':
				self.symbol.setText(self.symbol_list.currentItem().text())
				
			# max_trade = get_max(self.symbol.text())
			# if int(self.open_cap_rate.text()) != 1:
				# max_temp = int(int(self.open_cap_rate.text()) / 100 * max_trade)
				# print(max_temp)
			rows = [[self.symbol.text(),open_action,self.open_cap_rate.text(),self.open_cap_lever.text(),
			self.open_toMA.text(),self.close_toMA.text(),self.open_freq.text(),self.close_freq.text(),
			self.open_gap.text(),self.close_hold.text(),with_str,self.ma_n_open.text(),self.ma_n_close.text(),
			self.long_limit.text(),'True']]

			if self.symbol.text() not in list_ok:
				print('\n Save failed , Please use symbol in the list below \n',self.symbol.text(), ' not in \n\n', list_ok)
				return None
			
			df = pd.DataFrame(rows, columns=config_df)
			df.to_csv('config/'+self.symbol.text()+'.csv', index=False, mode='w',columns=config_df)
			df_total = df_total.append(df)
			print(df_total)

			# old_item = self.symbol_list.currentItem()
			# self.symbol_list.setCurrentItem(old_item)
			
			self.symbol_list.clear()
			symbols = file_name_walk('config/')
			if len(symbols)>0:
				for i in range(len(symbols)):
					symbols[i] = symbols[i].replace('.csv','')			
					self.symbol_list.addItems([symbols[i]])
					print([symbols[i]])
			start_list.append(self.symbol.text())
			# self.config_list.clear()
			# self.config_list.addItems(rows[0])
			self.config_list.addItems([self.symbol.text() + '  保存'])
			
			flag = '1'  # 0 real trading
			if self.Trd.isChecked():
				flag = '1'
			accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
			result = accountAPI.set_leverage(instId=self.symbol.text(), lever=self.open_cap_lever.text(), mgnMode='isolated')
			print(result)
			

		elif btn.text() == '&Y 全部开始':			
			df_cfg = read_config()
			print('\n len\t',len(df_cfg), '\t df_cfg \n \t\t\t\t\tBegin trading !\n', df_cfg['symbol'])
			
			if (sum(df_cfg.isnull().sum()) > 0):
				print(' conifg isnull ! ', k)
				return
			futu_freq = [1,3,5,15,30,60,2,4,10,120,180,240,360,480,720,1440]	
			if float(self.open_freq.text()) not in futu_freq or float(self.close_freq.text()) not in futu_freq :
				print(' Frequency minute is wrong ! ', k)
				return
				
			for i in range(len(list(df_cfg['symbol']))):	
				df = df_cfg[df_cfg['symbol'] == df_cfg['symbol'].iloc[i]]
				df.at[0, ['stop']] = 'False'
				df.to_csv('config/'+df_cfg['symbol'].iloc[i]+'.csv', index=False, mode='w',columns=config_df)
			self.config_list.addItems(['全部开始'])		
			k=0
		elif btn.text() == '&Q 全部停止':
			k=-1
			stop_all()
			self.config_list.addItems(['全部停止'])	
			
		elif btn.text() == '&H 全部平仓' :
			print('\n Clear all orders \n')
			df_clr = clear_all('all')
			if len(df_clr)>0:
				for i in range(len(df_clr)):
					self.trade_list.addItems([df_clr['symbol'].iloc[i]+' '+df_clr['act'].iloc[i]+' '+str(df_clr['quantity'].iloc[i])+' '+df_clr['oc'].iloc[i]])
			self.config_list.addItems(['全部平仓'])	
		elif btn.text() == '单个开始':
			if self.symbol_list.currentItem() is None:
				print('None return')
				self.config_list.addItems(['错误：未选取代码']);return
			print('start \t', self.symbol_list.currentItem().text())			
			df_cfg = read_config()			
			df = df_cfg[df_cfg['symbol'] == self.symbol_list.currentItem().text()]
			df.at[0, ['stop']] = 'False';	print(df['stop'])
			df.to_csv('config/'+self.symbol_list.currentItem().text()+'.csv', index=False, mode='w',columns=config_df)
			k=0
			self.config_list.addItems([self.symbol_list.currentItem().text() + '  单个开始'])	
		elif btn.text() == '单个停止':
			if self.symbol_list.currentItem() is None:
				print('None return')
				self.config_list.addItems(['错误：未选取代码']);return
			print('stop \t',self.symbol_list.currentItem().text())
			df_cfg = read_config()			
			df = df_cfg[df_cfg['symbol'] == self.symbol_list.currentItem().text()]
			df.at[0,'stop'] = 'True';	print(df['stop'])
			df.to_csv('config/'+self.symbol_list.currentItem().text()+'.csv', index=False, mode='w',columns=config_df)
			self.config_list.addItems([self.symbol_list.currentItem().text() + '  单个停止'])	
			
		elif btn.text() == '单个平仓':
			if self.symbol_list.currentItem() is None:
				print('None return')
				self.config_list.addItems(['错误：未选取代码']);return
			self.config_list.addItems([self.symbol_list.currentItem().text() + '  单个平仓'])	
			print('\n Clear '+self.symbol_list.currentItem().text()+'\n')
			clear_all(self.symbol_list.currentItem().text())		

	def closeEvent(self, event):
		stop_all()
		sys.exit()
			
	def initUI(self):
		self.backend = BackendThread()
		self.backend.update_date.connect(self.handleDisplay)
		self.thread = QThread()
		self.backend.moveToThread(self.thread)
		self.thread.started.connect(self.backend.run)
		self.thread.start()		
		
	def handleDisplay(self, data):
		global ospath, config_df, df_total, min2, k, symbols, df_cfg, start_list, stop_list, df_one
		comb=''+str(datetime.now())[11:19];		self.lb_Time.setText(comb);

		if self.cb1.isChecked()==True:			
			self.cb1.setChecked(False)
			f=open(r'str.csv','w');f.write('');f.close();
			f=open(r'error.csv','w');f.write('');f.close();		print('clear error.csv log')

		if stop_list==[]:
			stop_list.append(1)
			stop_all()

		if self.symbol_list.count()==0:
			self.symbol_list.clear()
			symbols = file_name_walk('config/')
			if len(symbols)>0:
				for i in range(len(symbols)):
					symbols[i] = symbols[i].replace('.csv','')			
					self.symbol_list.addItems([symbols[i]])

		if (k==-1 or k==0) or k%3==0:
			df_one = df_one.append(read_local_last())#'symbol','act','quantity','oc
			if len(df_one) == 0:return
			if len(df_one)>1 and (df_one['time_key'].iloc[-2] == df_one['time_key'].iloc[-1])==False:
				self.trade_list.addItems([df_one['symbol'].iloc[-1]+' '+df_one['act'].iloc[-1]+' '+str(df_one['quantity'].iloc[-1])+' '+df_one['oc'].iloc[-1]])

			if len(df_one)>9:
				df_one = df_one.iloc[-9:]

			count = self.trade_list.count()
			if count>1 and k!=-2:
				try:
					if self.trade_list.item(count-2).text() == self.trade_list.item(count-1).text():
						stop_all()
						# playsound('alert.mp3')
						k = -2
						self.trade_list.clear()
				except:
					print('alert error')

		if k%10 == 0:
			vsb = self.config_list.verticalScrollBar()	
			if vsb.value() <= vsb.maximum():vsb.setValue(vsb.value() + 2)	
			vsb = self.trade_list.verticalScrollBar()	
			if vsb.value() <= vsb.maximum():vsb.setValue(vsb.value() + 2)
		if k != -2:
			k += 1
#############

if __name__ == '__main__':
	app = QApplication(sys.argv)
	win = Window()	# win.setWindowFlags(Qt.WindowMinimizeButtonHint)
	win.move(680,0)
	win.show()
	sys.exit(app.exec_())