#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industrie
from board import *
from datetime import datetime
import adafruit_dht
import schedule
import time
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="Nature38:built:"
)

print(mydb)

SENSOR_PIN = D17
dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)
now = datetime.now()


def job():
    try:
        temperature_c = dht11.temperature
        time.sleep(1)
        humidity = dht11.humidity
        time.sleep(1)

        print(f"Humidity = {humidity:.2f}%")
        print(f"Temperature = {temperature_c:.2f}°C")

    except RuntimeError:
        print("sucks to be you")


schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
