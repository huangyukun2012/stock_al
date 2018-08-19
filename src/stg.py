# -*- coding: utf-8 -*-
# filename: stg.py

class Strategy:
	def __init__(self) :
		self.low_price_ = -1.0
		self.high_price_ = -1.0
		self.exchange_rate_ = -1.0
		self.action = 1 #buy
		self.stock_no = ""
		self.interval = 0 # unit is min
		self.last_scheduled_time = 0 #timestamp in milliseconds.
		return
