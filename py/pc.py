import numpy as np
import cv2
import os
import ssl
import geopy
from geopy import geocoders
from geopy.geocoders import Nominatim
import csv


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


def count_faces(image_path):
    face_cascade = cv2.CascadeClassifier('/Users/anastasia/Desktop/GWU/anastasija/py/haarcascade_frontalface_default.xml')

    image = cv2.imread(image_path) #'../data/photo1.jpg'
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    faces = face_cascade.detectMultiScale(grayImage)
 
    print(type(faces))
 
    if len(faces) == 0:
        print("No faces found")

    else:
        #print(faces)
        #print(faces.shape)
        print("Number of faces detected: " + str(faces.shape[0]))
 
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
        cv2.rectangle(image, ((0,image.shape[0] -25)),(270, image.shape[0]), (255,255,255), -1)
        cv2.putText(image, "Number of faces detected: " + str(faces.shape[0]), (0,image.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,0), 1)

        cv2.imshow('Image with faces',image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return faces.shape[0]


def readwrite_data():
    directory = '../data/photos/'
    #face_cascade = cv2.CascadeClassifier('/Users/anastasia/Desktop/GWU/anastasija/py/haarcascade_frontalface_default.xml')

    rows = {}
    fam = 1
    for entry in os.scandir(directory):
        #print(entry.path)
        fc = count_faces(entry.path)
        print("Enter city (or address), last name (e.g.: Ulaanbaatar,Smith):")
        inp = input()
        if (len(inp) == 0):
            break
        else:
            inp = inp.split(',')
            findex = "family" + str(fam)
            lat, lon = geoloc(inp[0])
            inp01 = [lat, lon]
            fc = [fc]
            rows[findex] = inp + fc + inp01
        fam += 1
    return rows


def write_to_csv(year):
    rows = readwrite_data()
    with open('../data/photo_data_' + year +'.csv', mode='a') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in rows:
            data_writer.writerow(rows[row])


#print(readwrite_data())
write_to_csv('2018')
#count_faces()

