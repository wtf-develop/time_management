import pymysql

# Database access information
mydb_connection = pymysql.connect(
        host="localhost",
        database='reminder',
        user="root",
        passwd=""
)

# check write folder permissions.
# last slash '/' - REQUIRED!!!
logs_path = '/var/log/planme/'
enable_logging = True

# enable GZIP compression for JSON APIs
enable_gzip = True

# ---------------- Don't change code below ----------------
# ---------------- Don't change code below ----------------
# ---------------- Don't change code below ----------------
# ---------------- Don't change code below ----------------
# ---------------- Don't change code below ----------------
# ---------------- Don't change code below ----------------
mydb = mydb_connection.cursor(cursor=pymysql.cursors.DictCursor)
mydb.execute("SET NAMES 'utf8mb4'")
