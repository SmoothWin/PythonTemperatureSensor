from .DbData import DBData
from Models.Humidity import Humidity


class DbHumidity:
    # Need to import the other class
    dta = DBData()

    def select_all_humidities(self):
        return self.dta.execute_select_query("humidity")

    # def select_book(self, d : int):
    #     pass

    def insert_humidity(self, humidity: Humidity):
        return self.dta.execute_insert_query("humidity", params=humidity)

    def delete_all_humidities(self):
        return self.dta.execute_delete_query("humidity")
