import strategy.okex as okex
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from termcolor import colored

constants = {'spot_commission_rate': Decimal(0.00045),
             'future_commission_rate': Decimal(0.00045),
             'spot_daily_interest_rate': Decimal(0.001),
             'spot_leverage': Decimal(3),
             'future_leverage': Decimal(10)}


def calculate_expire_date():
	# today = datetime.today()
	utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
	today = utc_now.astimezone(timezone(timedelta(hours=8)))
	this_sunday = today + timedelta(6 - today.weekday())
	next_friday = this_sunday + timedelta(5)
	next_friday = next_friday.replace(hour=16,
	                                  minute=0,
	                                  second=0,
	                                  microsecond=0)
	return next_friday


def calculate_interest_days(expire_date):
	today = datetime.today()
	interest_hours = (expire_date - today).total_seconds() / 3600
	return interest_hours // 24 + 1


def calculate_annulized_return_rate(profit, cost, days):
	daily_interest = (profit / cost + 1) ** (1 / Decimal(days)) - 1
	return (1 + daily_interest) ** 365


def get_calculate_signals_func(calc_exp_date, channel, color):

	def calculate_signals(spot_ticker, spot_depth, future_ticker, future_depth):
		spot_buy_price = spot_ticker['buy']
		spot_sell_price = spot_ticker['sell']
		future_buy_price = future_ticker['buy']
		future_sell_price = future_ticker['sell']

		if spot_sell_price > future_buy_price:
			signal = long_future_short_spot(spot_sell_price, future_buy_price, calc_exp_date)
			print(colored(channel + ' Long Future Short Spot',color))
			print(signal)
		elif spot_buy_price < future_sell_price:
			print(colored(channel + ' Short Future Long Spot', color))
			signal = short_future_long_spot(spot_buy_price, future_sell_price, calc_exp_date)
			print(signal)
		else:
			return
	return calculate_signals


# long future while short spot
def long_future_short_spot(spot_price, future_price, calc_exp_date_func):
	future_leverage = constants['future_leverage']
	spot_leverage = constants['spot_leverage']
	future_commission_rate = constants['future_commission_rate']
	spot_commission_rate = constants['spot_commission_rate']
	spot_interest_rate = constants['spot_daily_interest_rate']

	# Calculate cost for long future order
	future_margin = okex.margin(future_price, 1, future_leverage)
	future_commission = okex.commission(future_price, 1, future_commission_rate)

	# Calculate number of days until future expire
	expire_date = calc_exp_date_func()
	interest_days = calculate_interest_days(expire_date)

	# Calculate spot margin and commission and interest paid
	spot_margin = okex.margin(spot_price, 1, spot_leverage)
	spot_commission = okex.commission(spot_price, 1, spot_commission_rate)
	spot_interest = okex.interest(spot_price - spot_margin,
	                              spot_interest_rate,
	                              Decimal(interest_days))

	# Calculate total cost for executing the order
	total_cost = future_margin + future_commission \
	             + spot_margin + spot_commission + spot_interest
	net_profit = future_price - spot_price
	return_rate = calculate_annulized_return_rate(net_profit,
	                                              total_cost,
	                                              interest_days)
	return {'Spot Margin': spot_margin,
	        'Spot Commission': spot_commission,
	        'Spot Interest': spot_interest,
	        'Future Margin': future_margin,
	        'Future Commission': future_commission,
	        'Annualized Return': return_rate}


def short_future_long_spot(spot_price, future_price, calc_exp_date_func):
	future_leverage = constants['future_leverage']
	spot_leverage = constants['spot_leverage']
	future_commission_rate = constants['future_commission_rate']
	spot_commission_rate = constants['spot_commission_rate']
	spot_interest_rate = constants['spot_daily_interest_rate']

	# Calculate cost for short future order
	future_margin = okex.margin(future_price, 1, future_leverage)
	future_commission = okex.commission(future_price, 1, future_commission_rate)

	# Calculate number of days until future expire
	expire_date = calc_exp_date_func()
	interest_days = calculate_interest_days(expire_date)

	# Calculate spot long margin and commission and interest paid
	spot_margin = okex.margin(spot_price, 1, spot_leverage)
	spot_commission = okex.commission(spot_price, 1, spot_commission_rate)
	spot_interest = okex.interest(spot_price - spot_margin,
	                              spot_interest_rate,
	                              Decimal(interest_days))

	# Calculate total cost for executing the order
	total_cost = future_margin + future_commission \
	             + spot_margin + spot_commission + spot_interest
	net_profit = future_price - spot_price
	return_rate = calculate_annulized_return_rate(net_profit,
	                                              total_cost,
	                                              interest_days)
	return {'spot_price': spot_price,
	        'future_price': future_price,
	        'Spot Margin': spot_margin,
	        'Spot Commission': spot_commission,
	        'Spot Interest': spot_interest,
	        'Future Margin': future_margin,
	        'Future Commission': future_commission,
	        'Annualized Return': return_rate}
