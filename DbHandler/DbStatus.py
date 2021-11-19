from Models.Status import Status
from DbHandler.DbData import DBData


class DbStatus:
    # Need to import the other class
    dta = DBData()

    def select_all_statuses(self):
        """ Get all status from humidity table .

                        :return: Dictionary of status
                        """
        return self.dta.execute_select_query("status")

    # def select_book(self, d : int):
    #     pass

    def insert_status(self, status: Status):
        """ Insert status into status table.

                                :return: Inserted row
                                """
        return self.dta.execute_insert_query("status", params=status)

    def delete_all_statuses(self):
        """ Delete all data from status table

                                        :return: Number of rows deleted
                                        """
        return self.dta.execute_delete_query("status")
