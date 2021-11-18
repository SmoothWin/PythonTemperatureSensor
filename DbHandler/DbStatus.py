from Models.Status import Status
from DbHandler.DbData import DBData


class DbStatus:
    # Need to import the other class
    dta = DBData()

    def select_all_statuses(self):
        return self.dta.execute_select_query("status")

    # def select_book(self, d : int):
    #     pass

    def insert_status(self, status: Status):
        return self.dta.execute_insert_query("status", params=status)

    def delete_all_statuses(self):
        return self.dta.execute_delete_query("status")
