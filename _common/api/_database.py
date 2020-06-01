import mysql.connector

mydb_connection = mysql.connector.connect(
    host="localhost",
    database='reminder',
    user="root",
    passwd=""
)

mydb = mydb_connection.cursor(dictionary=True)
mydb.execute("SET NAMES 'utf8mb4'")
