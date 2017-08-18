#!/usr/bin/python3
import csv
import glob
from datetime import datetime
import dateutil.relativedelta
from statistics import mean

one_month = dateutil.relativedelta.relativedelta(months=1)
for datafilename in glob.glob('*_data.csv'):
	metafilename = datafilename.replace('_data.csv', '_meta.txt')
	with open(datafilename, 'r') as datafile:
		datareader = csv.reader(datafile, delimiter=';')
		next(datareader, None) # skip header line
		# nice to have future feature: detect correct column number via
		# header line instead of hardcoding the columns below
		data = {}
		for row in datareader:
			month = datetime.strptime(row[1], '%Y%m%d')
			rainfall = row[5]
			if rainfall == -999: #error value
				continue
			data[month] = rainfall
		# find youngest 30 complete years
		end = max([d for d in data])
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
						monthly_data.append(float(data[d]))
				monthly_avg.append(mean(monthly_data))
