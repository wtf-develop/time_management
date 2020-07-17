import pymysql

# Database access information
# Alter tables sql-request should be permitted
# for this database and user
mydb_connection = pymysql.connect(
        host="localhost",
        database='reminder',
        user="root",
        passwd=""
)

# ATTENTION ! ACHTUNG ! ВНИМАНИЕ !
# Must be ALWAYS "False" on real server
# For developers only to special debug
# last request that was send to some api
debug = True  # debug = False # for production servers

# Log some actions and errors to special folder.
# if you don't want to store this information,
# just set: enable_logging = False
# -- Check write folder permissions.
# -- last slash '/' - REQUIRED!!!
logs_path = '/var/log/planme/'
enable_logging = True

# enable GZIP compression for JSON APIs response
# if you will have some network problems with
# browsers or mobile application you can try
# set it to False.
enable_gzip = True

# Server token hash key.
# Don't have too much sense. Just make token
# incompatible between different servers.
# You can also reset all token sessions by
# changing this value to something else.
# All mobile and web-users will need to re-login
server_token_key = 'WASSUP!'

# How many month server will keep information
# about not active user. If he don't connect from app
# and don't open login form longer then this count
# of month all information about user will be removed.
# This is not exact time, but this is minimum
keep_user_data_month = 12

#
#
# ---------------- Don't change code below ----------------
# ---------------- Don't change code below ----------------
# ---------------- Don't change code below ----------------
# ---------------- Don't change code below ----------------
# ---------------- Don't change code below ----------------
# ---------------- Don't change code below ----------------
#
#
mydb = mydb_connection.cursor(cursor=pymysql.cursors.DictCursor)
mydb.execute("SET NAMES 'utf8mb4'")
