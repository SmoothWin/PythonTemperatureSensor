from DbHandler.DbData import DBData
from Models import Temperature


class DbTemperature:
    # Need to import the other class
    dta = DBData()

    def select_all_temperatures(self):
        return self.dta.execute_select_query("temperature")

    # def select_book(self, d : int):
    #     pass

    def insert_temperature(self, temperature: Temperature):
        return self.dta.execute_insert_query("temperature", params=temperature)

    def delete_all_temperatures(self):
        return self.dta.execute_delete_query("temperature")
