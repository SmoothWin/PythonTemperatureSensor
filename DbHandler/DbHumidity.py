from .DbData import DBData
from Models.Humidity import Humidity


class DbHumidity:
    # Need to import the other class
    dta = DBData()


    def select_all_humidities(self):
        """ Get all humidities from humidity table .

        :return: Dictionary of humidites
        """
        return self.dta.execute_select_query("humidity")

    def insert_humidity(self, humidity: Humidity):
        """ Insert humidity into humidity table.

                :return: Inserted row
                """
        return self.dta.execute_insert_query("humidity", params=humidity)

    def delete_all_humidities(self):
        """ Delete all data from humidity table

                        :return: Number of rows deleted
                        """
        return self.dta.execute_delete_query("humidity")
