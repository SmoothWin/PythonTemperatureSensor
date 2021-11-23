#!/home/pi/homeWork/pythonProject2/venv/bin/python

import json
import os
import time

import requests
import schedule
from board import *
import adafruit_dht
from datetime import datetime

from DbHandler.DbStatus import DbStatus  # query class from the DBhandler
from DbHandler.DbHumidity import DbHumidity  # query class from the DBhandler
from DbHandler.DbTemperature import DbTemperature  # query class from the DBhandler
from Models.Humidity import Humidity # model class from Models
from Models.Status import Status # model class from Models
from Models.Temperature import Temperature # model class from Models
from cryptography.fernet import Fernet
from dotenv import load_dotenv  # needed in order to load environment secrets such as the symmetric key for the decryption

load_dotenv()

SENSOR_PIN = D17
dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)
humidity = DbHumidity() # Database query class for the Humidity data
my_time = datetime.now() # Global variable used to get the same time in all of the inserts, regardless the delays
temperature = DbTemperature() # Database query class for the Temperature data
status = DbStatus() # Database query class for the Status history data


def get_time_now():
    global my_time
    my_time = datetime.now()


def add_status():
    my_statue = check_status() # Using requests.get, get a response from a web app
    status_insert = Status(my_statue, my_time) # create an object of status class
    insert_status = status.insert_status(status_insert) # perform an insert using Database query class DBStatus
    return insert_status


def add_temperature():
    while True:
        try:
            time.sleep(2)
            temperature_c = dht11.temperature # read temperature using adafruit library
            break
        except RuntimeError:
            print("Error, while reading the temperature")
    temperature_insert = Temperature(temperature_c, my_time) # create an object of temperature class
    insert_temp = temperature.insert_temperature(temperature_insert) # perform an insert using Database query class DBTemperature
    return insert_temp


def add_humidity():
    while True:
        try:
            time.sleep(2)
            humidity_percent = dht11.humidity # read humidity using adafruit library
            break
        except RuntimeError:
            print("Error, while reading the humidity")

    humidity_insert = Humidity(humidity_percent / 100, my_time) # create an object of humidity class
    insert_hum = humidity.insert_humidity(humidity_insert) # perform an insert using Database query class DBTHumidity
    return insert_hum


def select_all_temperatures():
    select_all_temps = temperature.select_all_temperatures() # This is a select for getting temperatures from the db connection
    return select_all_temps


def select_all_humidities():
    select_all_hums = humidity.select_all_humidities() # This is a select for getting the humidities from the db connection
    return select_all_hums


def select_all_statuses():
    select_all_stats = status.select_all_statuses() # This is a select for getting the status history from the db connection
    return select_all_stats


def get_web_db_status():
    r = requests.get("https://pythontemperaturetracker.herokuapp.com") # perform a get request and return status
    return r.status_code


def check_status():
    web_db_status = get_web_db_status()
    if web_db_status == 200: # check if status is 200, if it is, 1 - true, if not 0 - false
        return 1
    else:
        return 0


def delete_all_data():
    humidities_deleted = humidity.delete_all_humidities() # This is a delete for deleting all humidities from the db connection
    temperatures_deleted = temperature.delete_all_temperatures() # This is a delete for deleting the temperatures  from the db connection
    statuses_deleted = status.delete_all_statuses() # This is a delete for deleting the status history from the db connection


def post_into_web_app():
    f = Fernet(os.environ.get('REQUEST_SECRET'))
    my_data = assemble_json()

    my_data = json.dumps(my_data, indent=2, default=str)
    my_data_dict = json.loads(my_data)
    string = ""
    for i in my_data_dict.keys():
        string += str(my_data_dict[i])

    encrypted_data = f.encrypt(bytes(string, 'ASCII'))

    header = {"security-check": encrypted_data.decode("UTF-8"), "Content-type": "application/json"}
    url = "https://pythontemperaturetracker.herokuapp.com/api/send"

    x = requests.post(url, data=my_data, headers=header)
    return x


def assemble_json(): # This method gell all of the data, removes the ID field from each of them, then converts status from tinyInt to a bool and the assemble it into one big dictionnary
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


schedule.every(20).minutes.do(job) # Using schedule library I schedule my program to perform my job method each 20 minutes
schedule.every(40).minutes.do(send_web_app_data) # Using schedule library I schedule my program to perform my send_web_app_data method each 40 minutes

while True:
    schedule.run_pending()
    time.sleep(1)
