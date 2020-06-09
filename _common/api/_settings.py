import mysql.connector

# Database access information
mydb_connection = mysql.connector.connect(
    host="localhost",
    database='reminder',
    user="root",
    passwd=""
)


# --- Don't change code below ---
mydb = mydb_connection.cursor(dictionary=True)
mydb.execute("SET NAMES 'utf8mb4'")
