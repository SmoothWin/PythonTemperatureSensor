import json
import os
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
from dotenv import load_dotenv

load_dotenv()

SENSOR_PIN = D17
dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)
humidity = DbHumidity()
my_time = datetime.now()
temperature = DbTemperature()
status = DbStatus()


def get_time_now():
    global my_time
    my_time = datetime.now()


def add_status():
    my_statue = check_status()
    status_insert = Status(my_statue, my_time)
    insert_status = status.insert_status(status_insert)
    return insert_status


def add_temperature():
    while True:
        try:
            time.sleep(2)
            temperature_c = dht11.temperature
            break
        except RuntimeError:
            print("Error, while reading the temperature")
    temperature_insert = Temperature(temperature_c, my_time)
    insert_temp = temperature.insert_temperature(temperature_insert)
    return insert_temp


def add_humidity():
    while True:
        try:
            time.sleep(2)
            humidity_percent = dht11.humidity
            break
        except RuntimeError:
            print("Error, while reading the humidity")

    humidity_insert = Humidity(humidity_percent / 100, my_time)
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
    f = Fernet(os.environ.get('REQUEST_SECRET'))
    my_data = assemble_json()

    my_data = json.dumps(my_data, indent=2, default=str)
    my_data_dict = json.loads(my_data)
    string = ""
    for i in my_data_dict.keys():
        string += str(my_data_dict[i])
    print(string)
    print(my_data_dict)
    print(my_data)
    encrypted_data = f.encrypt(bytes(string, 'ASCII'))
    print(encrypted_data.decode("UTF-8"))

    header = {"security-check": encrypted_data.decode("UTF-8"), "Content-type": "application/json"}
    url = "https://pythontemperaturetracker.herokuapp.com/api/send"

    x = requests.post(url, data=my_data, headers=header)
    return x


def assemble_json():
    all_temperatures = select_all_temperatures()
    for t in all_temperatures:
        t.pop("ID")
    all_humidities = select_all_humidities()
    for h in all_humidities:
        h.pop("ID")
    all_statuses = select_all_statuses()
    for s in all_statuses:
        s.pop("ID")
        s["online"] = bool(s.get("online"))
    all_data = {"temperature": all_temperatures, "humidity": all_humidities, "status": all_statuses}

    return all_data


def job():
    get_time_now()
    add_humidity()
    add_status()
    add_temperature()


def send_web_app_data():
    if check_status():
        post_into_web_app()
        delete_all_data()


schedule.every(5).minutes.do(job)
schedule.every(10).minutes.do(send_web_app_data)

while True:
    schedule.run_pending()
    time.sleep(1)

