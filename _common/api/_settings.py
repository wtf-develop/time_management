import pymysql


# Database access information
mydb_connection = pymysql.connect(
    host="localhost",
    database='reminder',
    user="root",
    passwd=""
)
enable_logging = True
# logs_path: last '/' - REQUIRED!!!
logs_path = '/var/log/planme/'  # check folder permissions.


# --- Don't change code below ---
# --- Don't change code below ---
# --- Don't change code below ---
# --- Don't change code below ---
# --- Don't change code below ---

mydb = mydb_connection.cursor(cursor=pymysql.cursors.DictCursor)
mydb.execute("SET NAMES 'utf8mb4'")
