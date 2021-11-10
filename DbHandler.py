import mysql.connector
from datetime import datetime


def db_insert(table_name, field_name, field_value):
    mydb = mysql.connector.connect(host="localhost", user="admin", password="Nature38:built:", database="dht_db")
    now = datetime.now()
    mycursor = mydb.cursor()
    sql = f"INSERT INTO {table_name} ({field_name},time) VALUES (%s, %s)"
    val = (field_value, now)
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return mycursor.rowcount


def db_get_all(table_name):

    mydb = mysql.connector.connect(host="localhost", user="admin", password="Nature38:built:", database="dht_db")

    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT * FROM {table_name}")

    myresult = mycursor.fetchall()
    mydb.close()
    return myresult



