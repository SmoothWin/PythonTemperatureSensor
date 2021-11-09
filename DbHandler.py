import mysql.connector
from datetime import datetime


mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="Nature38:built:"
)


def db_insert(table_name, field_name, field_value):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    mycursor = mydb.cursor()
    sql = f"INSERT INTO {table_name} ({field_name}) VALUES (%s, %s)"
    val = (field_value)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")
