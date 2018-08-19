import urllib,urllib2
import MySQLdb as mdb
import threadpool
import time
import Queue
import datetime
import threading2 as threading

price_detail_url='http://image.sinajs.cn/newchart/min/n/sh'
#sz, sh
G_stock_number_queue = Queue.Queue(maxsize=4000)
G_duration = 3

class dbManager:
	def insert_t(self, sql=""):
		cursor = self.db.cursor()
		cursor.execute(sql)
		#data = cursor.fetchone()
		cursor.execute(sql)
		self.db.commit()
		#print data
		self.db.close()
	def __init__(self, host, username, password, database):
		self.db=mdb.connect(host, username, password, database, charset='utf8')
	
		
class Stock_deal_info :
	def __init__(self, number_str):
		self.name = ""
		self.start_price= 1.0
		self.end_price= 1.0
		self.current_price = 1.0
		self.highest_price = 1.0
		self.lowest_price = 1.0
		self.unit_of_deal = 10
		self.amount_of_deal = 10.0
		self.rdate = datetime.date.today()
		self.delta_price_percent = 0.32
		self.change_rate = 0.64
		self.main_in = 11.1 #*10000
		self.main_out = 11.1
		self.main_in_div_total = 1.1
		self.no= number_str
		
def get_data_from_sina(number, stock):
	sinaurl='http://hq.sinajs.cn/list='
	number = format_prefix(number)
	req = urllib2.Request(sinaurl + number)
	
	res = urllib2.urlopen(req)
	res = res.read()
	ele_array = res.split(',')
	#0:name, 1:start_price, 2:end_price, 3:current_price, 4:highest_price, 5:lowest_price, 6:buy1, 7:sell1
	#8:unit_of_deal, 9:amount_of_deal, 10~29: buy-sell-details
	#30:date, 31:time
	print ele_array
	stock.start_price= float(ele_array[1])
	stock.end_price= float(ele_array[2])
	stock.current_price = float(ele_array[3])
	stock.highest_price = float(ele_array[4])
	stock.lowest_price = float(ele_array[5])
	stock.unit_of_deal = int(ele_array[8])
	stock.amount_of_deal = float(ele_array[9])
	stock.rdate = ele_array[30]

def get_data_from_tx(number, stock):
	txurl='http://qt.gtimg.cn/q='
	number = format_prefix(number)
	req = urllib2.Request(txurl + number)
	res = urllib2.urlopen(req)
	res = res.read()
	ele_array = res.split('~')
	print ele_array
	stock.delta_price_percent = float(ele_array[32])
	stock.exchange_rate = float(ele_array[38])

def format_prefix(number):
	#600, 601, 603 shanhai
	#300 startup company
	#000 shenzhen
	#002 middle and small
	prefix = number[0:3]
	if prefix == "600" or prefix == "601" or prefix == "603" or prefix == "300" :
		return "sh" + number
	elif prefix == "000" or prefix == "002":
		return "sz" + number
	return number

def get_major_data_from_tx(number, stock):
	txmainurl='http://qt.gtimg.cn/q=ff_'
	number = format_prefix(number)
	req = urllib2.Request(txmainurl+ number)
	res = urllib2.urlopen(req)
	res = res.read()
	ele_array = res.split('~')
	print ele_array
	stock.main_in = float(ele_array[1])
	stock.main_out = float(ele_array[2])
	stock.main_in_div_total = float(ele_array[4])

def insert_into_stock_deal_daily(dbcnc, s):
	insert_str= """insert into stock_deal_daily(
	id, start_price, end_price, current_price, highest_price, lowest_price, unit_of_deal, amount_of_deal, rdate, main_in, main_out, main_in_delta_div_total, delta_price_percent, exchange_rate)
	values """
	main_in_delta_div_total = (s.main_in - s.main_out) * 10000 / s.amount_of_deal * 100
	value="'%s',%.2f,%.2f,%.2f,%.2f,%.2f,%d,%.2f,'%s',%.2f,%.2f,%.2f,%.2f,%.2f" % (s.no, s.start_price, s.end_price, s.current_price, s.highest_price, s.lowest_price, s.unit_of_deal, s.amount_of_deal, s.rdate, s.main_in, s.main_out, main_in_delta_div_total, s.delta_price_percent, s.exchange_rate)
	full_str = insert_str + "(" + value + ");"
	print full_str
	dbcnc.insert_t(full_str)

def read_stock_number(filename):
	print "read stock data from %s" % filename
	global G_stock_number_queue
	f = open(filename)
	line = f.readline()
	while line:
		G_stock_number_queue.put(line)
		print line
		line = f.readline()
	f.close
	print "waiting for next read"
	global timer
	timer = threading.Timer(G_duration, read_stock_number, ["/tmp/id"])
	timer.start()

def is_weekend_now():
	now=time.time()
	day=long(now)/86400
	index = (day +3) % 7 +1
	return index >= 6

def start_service():

if __name__ == "__main__":
	timer = threading.Timer(2, read_stock_number, ["/tmp/id"])
	timer.start()
	start_service()

