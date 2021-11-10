#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industrie
import sys

from board import *
# from datetime import datetime
import adafruit_dht
# import schedule
# import time
from pylint.lint import Run

import DbHandler

SENSOR_PIN = D17
dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)
try:
    temperature_c = dht11.temperature
except RuntimeError:
    print("sheesh")
    sys.exit(1)

insert_result = DbHandler.db_insert("temperature","temperature",temperature_c)
print(insert_result, "record inserted.")

myresult = DbHandler.db_get_all("temperature")
for x in myresult:
    print(x)

# def job():
#     try:
#         temperature_c = dht11.temperature
#         time.sleep(1)
#         humidity = dht11.humidity
#         time.sleep(1)
#
#         print(f"Humidity = {humidity:.2f}%")
#         print(f"Temperature = {temperature_c:.2f}°C")
#
#     except RuntimeError:
#         print("sucks to be you")
#
#
# schedule.every(10).seconds.do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
