import os
import sys
import backtrader as bt
import backtrader.feeds as btfeeds
import yfinance as yf
from datetime import datetime

class MAstrategy(bt.Strategy):
	# when initializing the instance, create a 100-day MA indicator using the closing price
	def __init__(self):
		self.ma = bt.indicators.SimpleMovingAverage(self.data.close, period=100)
		self.order = None
 
	def next(self):
		if self.order:
			return
		if not self.position: # check if you already have a position in the market
			if (self.data.close[0] > self.ma[0]) & (self.data.close[-1] < self.ma[-1]):
				self.log('Buy Create, %.2f' % self.data.close[0])
				self.order = self.buy(size=10) # buy when closing price today crosses above MA.
			if (self.data.close[0] < self.ma[0]) & (self.data.close[-1] > self.ma[-1]):
				self.log('Sell Create, %.2f' % self.data.close[0])
				self.order = self.sell(size=10)  # sell when closing price today below MA
		else:
		# This means you are in a position, and hence you need to define exit strategy here.
			if len(self) >= (self.bar_executed + 4):
				self.log('Position Closed, %.2f' % self.data.close[0])
				self.order = self.close()
 
	# outputting information
	def log(self, txt):
		dt=self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))
   
	def notify_order(self, order):
		if order.status == order.Completed:
			if order.isbuy():
				self.log(
				"Executed BUY (Price: %.2f, Value: %.2f, Commission %.2f)" %
				(order.executed.price, order.executed.value, order.executed.comm))
			else:
				self.log(
				"Executed SELL (Price: %.2f, Value: %.2f, Commission %.2f)" %
				(order.executed.price, order.executed.value, order.executed.comm))
			self.bar_executed = len(self)
		elif order.status in [order.Canceled, order.Margin, order.Rejected]:
			self.log("Order was canceled/margin/rejected")
		self.order = None

def execute(fromdate, todate):
	# if __name__ == '__main__':

	# Create a cerebro instance, add our strategy, some starting cash at broker and a 0.1% broker commission
	cerebro = bt.Cerebro()
	cerebro.addstrategy(MAstrategy)
	cerebro.broker.setcash(10000)
	cerebro.broker.setcommission(commission=0.001)

	data = bt.feeds.PandasData(dataname=yf.download("EURUSD=X"), fromdate=fromdate, todate=todate)
	
	cerebro.adddata(data)
	

	# For creating the plot
	# fromDate = datetime(1000, 1, 1, 00, 00, 00)
	# toDate = datetime(3000, 1, 1, 23, 59, 59)

	# cerebro.plot(
	# 	start=fromDate,
	# 	end=toDate,
	# 	style='candlestick'
	# )
		
	return cerebro.run()