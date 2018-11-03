import csv
import sys
import geopy
from geopy import geocoders
from geopy.geocoders import Nominatim
import ssl

from imutils.object_detection import non_max_suppression                     
import numpy as np
import imutils
import cv2
import requests
import time
import argparse


def write_to_csv(year):
	rows = input_reader()
	with open('../data/data_' + year +'.csv', mode='a') as data_file:
		data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		for row in rows:
			data_writer.writerow(rows[row])


def input_reader():
	rows = {}
	fam = 1
	while True:
		print("Enter city (or address), last name, number of children, income (e.g.: Ulaanbaatar,Smith,5,10000):")
		inp1 = input()
		if (len(inp1) == 0):
			break
		else:
			inp1 = inp1.split(',')
			findex = "family" + str(fam)
			lat, lon = geoloc(inp1[0])
			inp01 = [lat, lon]
			rows[findex] = inp1 + inp01
			child = 1
			while child <= int(inp1[2]):
				print("Enter child #" + str(child) + "'s name, age, gender (e.g.: John,9,M):")
				inp2 = input()
				if (len(inp2) == 0):
					break
				else:
					inp2 = inp2.split(',')
					cindex = findex + "_child" + str(child)
					inp02 = ["child" + str(child)]
					rows[cindex] = inp02 + inp2
					child += 1
			fam += 1
	return rows


def geoloc(locat):
	# Disable SSL certificate verification
	try:
		_create_unverified_https_context = ssl._create_unverified_context
	except AttributeError:
		pass
	else:
		ssl._create_default_https_context = _create_unverified_https_context
	geopy.geocoders.options.default_user_agent = 'my_app/1'
	geopy.geocoders.options.default_timeout = 7
	geolocator = Nominatim()
	location = geolocator.geocode(locat)
	return (location.latitude, location.longitude)




#print(geoloc("Khoroo 4 Ulaanbaatar"))
#Ерөнхий сайд А.Амарын гудамж


#write_to_csv("2018")

#rows = input_reader()
#for r in rows:
#	print(r)