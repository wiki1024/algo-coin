#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 21:46:05 2018

@author: yi
"""


def commission(price, quantity, commission_rate=0.00045):
	return price * quantity * commission_rate


def margin(price, quantity, leverage):
	return price * quantity / leverage


def interest(base_amount, interest_rate, days):
	total_interest = 0
	while True:
		daily_interest = base_amount * interest_rate
		# print(daily_interest)
		if days >= 15:
			total_interest += daily_interest * 15
			days -= 15
			base_amount += daily_interest * 15
		else:
			total_interest += daily_interest * days
			break
	return total_interest


if __name__ == '__main__':
	print(interest(10000, 0.01, 20))

