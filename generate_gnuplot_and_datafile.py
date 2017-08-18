#!/usr/bin/python3

import csv
import glob
from datetime import datetime
import dateutil.relativedelta
from statistics import mean
from collections import namedtuple
from math import floor, ceil
RT = namedtuple('RT', ['rain', 'temp'])

one_month = dateutil.relativedelta.relativedelta(months=1)
for datafilename in glob.glob('*_data.csv'):
	station_id = datafilename[0:5]
	metafilename = station_id+'_meta.txt'
	with open(metafilename, 'r', encoding='latin-1') as metafile:
		print(metafilename)
		metareader = csv.reader(metafile, delimiter=';')
		header_row = next(metareader)
		for n,col in enumerate(header_row):
			if col=='Stationshoehe':
				COL_ALTITUDE = n
			elif col=='Geogr.Breite':
				COL_LATITUDE = n
			elif col=='Geogr.Laenge':
				COL_LONGITUDE = n
			elif col=='Stationsname':
				COL_STATIONNAME = n
		for row in metareader:
			altitude = int(round(float(row[COL_ALTITUDE]),0))
			latitude = row[COL_LATITUDE]
			longitude = row[COL_LONGITUDE]
			stationname = row[COL_STATIONNAME]
			#not intelligent at all.
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
			rain = float(row[COL_RAIN])
			temp = float(row[COL_TEMP])
			if int(rain) == -999 or int(temp) == -999: #error value
				continue
			print(rain,temp)
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
						monthly_data.append(RT(float(data[d][0]),\
							float(data[d][1])))
				monthly_avg.append(RT(mean([m.rain for m in monthly_data]),\
					mean([m.temp for m in monthly_data])))
			yearly_avg = RT(mean([m.rain for m in monthly_avg]),\
					mean([m.temp for m in monthly_avg]))
			with open(station_id+'_data2.csv','w') as outfile:
				writer = csv.writer(outfile, delimiter='\t')
				writer.writerow([0,round(monthly_avg[11].rain,2),\
					round(monthly_avg[11].temp,2)])
				for n,avg in enumerate(monthly_avg):
					writer.writerow([n+1, round(avg.rain,2),\
						round(avg.temp,2)])
				writer.writerow([13,round(monthly_avg[0].rain,2),\
					round(monthly_avg[0].temp,2)])
				print(monthly_avg)
			with open('template.gpl', 'r') as templatefile:
				gnuplot = templatefile.read()
			context = {'SVGFILE': 'DWD_'+station_id+'_'+start.strftime('%Y')+'_'+end.strftime('%Y')+'.svg',\
				'TEMP_MIN': floor(min([m.temp for m in monthly_avg]+[m.rain/10 for m in monthly_avg])/5)*5,\
				'TEMP_MAX': ceil(max([m.temp for m in monthly_avg]+[m.rain/10 for m in monthly_avg])/5)*5,\
				'STATION_NAME':stationname,\
				'STATION_ID': station_id,\
				'ALTITUDE': altitude,\
				'LAT': latitude,\
				'LON': longitude,\
				'YEAR1': start.strftime('%Y'),\
				'YEAR2': end.strftime('%Y'),\
				'TEMP_AVG': round(mean([m.temp for m in monthly_avg]),1),\
				'RAIN_AVG': int(round(sum([m.rain for m in monthly_avg]),0)),\
				'DATAFILE': station_id+'_data2.csv'}
			context['TEMP_MIN'] = min([0,context['TEMP_MIN']])
			with open('DWD_'+station_id+'.gpl', 'w') as outfile:
				outfile.write(gnuplot.format(**context))
