import mysql.connector


class DBData:
    def __init__(self):
        try:
            self.config_file = "my.conf"
            self.connex = mysql.connector.connect(option_files=self.config_file)
        except mysql.connector.Error as e:
            print(e)
            self.connex.close()

    def execute_select_query(self, table_name, params=None):
        return_set = []
        cursor = self.connex.cursor(dictionary=True)
        if params is None:
            cursor.execute("select * from {}".format(table_name))
        else:
            where_clause = 'WHERE ' + 'AND'.join(['`' + k + '` = %s' for k in params.keys()])
            values = list(params.values())
            print(where_clause)
            sql = "SELECT * FROM {} {}".format(table_name, where_clause)
            print(sql)

            cursor.execute(sql, values)

        for x in cursor:
            return_set.append(x)

        cursor.close()

        return return_set

    def execute_insert_query(self, table_name, params=None):
        connex = self.connex
        cursor = connex.cursor(dictionary=True)
        try:

            sql = "INSERT INTO {} ({}) VALUES ({})".format(table_name,
                                                           ", ".join(params.to_dictionary().keys()),
                                                           ", ".join(
                                                               ["%s" for i in range(len(params.to_dictionary()))]))
            print(params.to_dictionary())
            cursor.execute(sql, list(params.to_dictionary().values()))

            self.connex.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print(err.msg())
            self.connex.close()

    def execute_delete_query(self, table_name, params=None):

        cursor = self.connex.cursor(dictionary=True)
        if params is None:
            cursor.execute("delete from {}".format(table_name))
        else:
            where_clause = 'WHERE ' + 'AND'.join(['`' + k + '` = %s' for k in params.keys()])
            values = list(params.values())
            print(where_clause)
            sql = "delete FROM {} {}".format(table_name, where_clause)
            print(sql)

            cursor.execute(sql, values)
            self.connex.commit()
        rows = cursor.rowcount
        cursor.close()
        return rows


