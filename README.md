# About

OpenSource personal time managment system. Server source code for [this Reminder application](https://play.google.com/store/apps/details?id=ru.mcsar.schedule) from GooglePlay

# Installation

1) Setup server environment (look "Server requrements")
2) Remove old source files if they exists
3) Open file **/_common/api/_database.py** and change database credentials
4) Run script **/zzz_install_and_then_remove_it.sh**
5) Remove all files with name **zzz_install_and_then_remove_it**.* with any extentions

For update process please start from step 2

# Server requrements
Can be any old personal computer. Or any modern dedicated server. You can try to install it even directly to your mobile device or router, if you know how to do this. 

### Python 3.3+ 
Or higher

### Apache2 
with CGI folder 
```
<VirtualHost *:80>
    <Directory /var/www/html>
        Options Indexes FollowSymLinks ExecCGI
        DirectoryIndex index.py, index.html
    </Directory>
    AddHandler cgi-script .py
    ...
    ...
</VirtualHost>
```

### Database
install MySQL or MariaDB 

Install driver for connections
```bash
pip3 install mysql-connector
```

# FAQ
- If you want to install this project somewhere and don't know how to do this: There are a lot of examples in Internet: Apache + MySQL + Python
- If you want to change/add/extend something: Do it byself and create merge request.
