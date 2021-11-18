import json
import time

import requests
import schedule
from board import *
import adafruit_dht
from datetime import datetime

from DbHandler.DbStatus import DbStatus
from DbHandler.DbHumidity import DbHumidity
from DbHandler.DbTemperature import DbTemperature
from Models.Humidity import Humidity
from Models.Status import Status
from Models.Temperature import Temperature
from cryptography.fernet import Fernet

SENSOR_PIN = D17
dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)
humidity = DbHumidity()
my_time = datetime.now()
temperature = DbTemperature()
status = DbStatus()


#
# def job():
#     try:
#         temperature_c = dht11.temperature
#         time.sleep(2)
#         humidity = dht11.humidity
#         time.sleep(2)
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


def add_status():
    my_statue = check_status()
    status_insert = Status(my_statue, my_time)
    insert_status = status.insert_status(status_insert)
    return insert_status


def add_temperature():
    try:
        time.sleep(2)
        temperature_c = dht11.temperature
    except RuntimeError:
        print("Error, while reading the temperature")
        time.sleep(4)
        temperature_c = dht11.temperature
    temperature_insert = Temperature(temperature_c, my_time)
    insert_temp = temperature.insert_temperature(temperature_insert)
    return insert_temp


def add_humidity():
    try:
        time.sleep(2)
        humidity_percent = dht11.humidity
    except RuntimeError:
        print("Error, while reading the humidity")
        time.sleep(4)
        humidity_percent = dht11.humidity
    humidity_insert = Humidity(humidity_percent, my_time)
    insert_hum = humidity.insert_humidity(humidity_insert)
    return insert_hum


def select_all_temperatures():
    select_all_temps = temperature.select_all_temperatures()
    return select_all_temps


def select_all_humidities():
    select_all_hums = humidity.select_all_humidities()
    return select_all_hums


def select_all_statuses():
    select_all_stats = status.select_all_statuses()
    return select_all_stats


def get_web_db_status():
    r = requests.get("https://pythontemperaturetracker.herokuapp.com")
    return r.status_code


def check_status():
    web_db_status = get_web_db_status()
    if web_db_status == 200:
        return 1
    else:
        return 0


def delete_all_data():
    humidities_deleted = humidity.delete_all_humidities()
    temperatures_deleted = temperature.delete_all_temperatures()
    statuses_deleted = status.delete_all_statuses()


def post_into_web_app():
    key = Fernet.generate_key()
    f = Fernet(key)
    my_data = assemble_json()
    encrypted_data = f.encrypt(bytes(str(list(my_data.values())), 'ASCII'))
    header = {"security-check": encrypted_data}
    url = "https://pythontemperaturetracker.herokuapp.com/api/send"

    x = requests.post(url, data=my_data, headers=header)
    return x


def assemble_json():
    all_temperatures = select_all_temperatures()
    all_humidities = select_all_humidities()
    all_statuses = select_all_statuses()
    all_data = {"humidities": all_humidities, "status": all_statuses, "temperatures": all_temperatures}
    return all_data


delete_all_data()

add_humidity()
add_status()
add_temperature()
results = post_into_web_app()
print(json.dumps(results.text, indent=2, default=str))
