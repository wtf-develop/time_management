import pymysql

# Database access information
mydb_connection = pymysql.connect(
    host="localhost",
    database='reminder',
    user="root",
    passwd=""
)


# --- Don't change code below ---
# cursorclass=pymysql.cursors.DictCursor
mydb = mydb_connection.cursor(cursor=pymysql.cursors.DictCursor)
mydb.execute("SET NAMES 'utf8mb4'")
