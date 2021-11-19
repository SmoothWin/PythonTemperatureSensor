from DbHandler.DbData import DBData
from Models import Temperature


class DbTemperature:
    # Need to import the other class
    dta = DBData()

    def select_all_temperatures(self):
        """ Get all temperatures from humidity table .

                :return: Dictionary of temperatures
                """
        return self.dta.execute_select_query("temperature")

    # def select_book(self, d : int):
    #     pass

    def insert_temperature(self, temperature: Temperature):
        """ Insert temperature into temperature table.

                        :return: Inserted row
                        """
        return self.dta.execute_insert_query("temperature", params=temperature)

    def delete_all_temperatures(self):
        """ Delete all data from temperature table

                                :return: Number of rows deleted
                                """
        return self.dta.execute_delete_query("temperature")
