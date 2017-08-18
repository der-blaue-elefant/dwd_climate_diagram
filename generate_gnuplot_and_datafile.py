#!/usr/bin/python3

import csv
import glob
from datetime import datetime
import dateutil.relativedelta
from statistics import mean
from collections import namedtuple
RT = namedtuple('RT', ['rain', 'temp'])

one_month = dateutil.relativedelta.relativedelta(months=1)
for datafilename in glob.glob('*_data.csv'):
	metafilename = datafilename.replace('_data.csv', '_meta.txt')
	with open(datafilename, 'r') as datafile:
		datareader = csv.reader(datafile, delimiter=';')
		header_row = next(datareader)
		for n,col in enumerate(header_row):
			if col=='MESS_DATUM_BEGINN':
				COL_MONTH = n
			elif col=='MO_TT':
				COL_TEMP = n
			elif col=='MO_RR':
				COL_RAIN = n
		data = {}
		for row in datareader:
			month = datetime.strptime(row[COL_MONTH], '%Y%m%d')
			rain = row[COL_RAIN]
			temp = row[COL_TEMP]
			if rain == '-999' or temp == '-999': #error value
				continue
			data[month] = RT(rain,temp)
		# find youngest 30 complete years
		try:
			end = max([d for d in data])
		except ValueError:
			continue
		for i in range(0,30*12):
			start = end - i*one_month
			if not start in data:
				break
		else:
			#complete 30 years found
			monthly_avg = []
			print (datafilename, start, end)
			for i in range(1,12+1):
				monthly_data = []
				for d in data:
					if int(d.strftime('%-m'))==i:
						monthly_data.append((float(data[d][0]),\
							float(data[d][1])))
				monthly_avg.append(RT(mean([m[0] for m in monthly_data]),\
					mean([m[1] for m in monthly_data])))
			with open(datafilename.replace('_data.csv', '_data2.csv'),'w') as outfile:
				writer = csv.writer(outfile, delimiter=';')
				for n,avg in enumerate(monthly_avg):
					writer.writerow([n+1, round(avg.rain,2), round(avg.temp,2)])
