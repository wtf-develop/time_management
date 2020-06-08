# About

OpenSource self-hosted personal time management system. Server source code was created for [this Reminder application](https://play.google.com/store/apps/details?id=ru.mcsar.schedule) from GooglePlay

# Installation

1) Setup server environment (look "Server requirements")
2) Remove old source files if they exists
3) Open file **/_common/api/_database.py** and change database credentials
4) Run script **/zzz_install_and_then_remove_it.sh**
5) Remove all files with name **zzz_install_and_then_remove_it**.* with any extensions

For update process please start from step 2

# Server requirements
Can be any old personal computer. Or any modern dedicated server. You can try to install it even directly to your mobile device or router, if you know how to do this and want to have fun.

### Python 3.3+
Or higher. While development it was v3.7

### Apache2
with CGI folder
```
<VirtualHost *:80>
    <Directory /var/www/html>
        Options +ExecCGI
        DirectoryIndex index.py, index.html
    </Directory>
    AddHandler cgi-script .py
    ...
    ...
</VirtualHost>
```

### Database
Install MySQL or MariaDB

And install recommended driver for Python
```bash
pip3 install mysql-connector
```

# FAQ
- If you want to install this project somewhere and don't know how to do this: there are a lot of examples in Google by request: Apache(CGI mode) + MySQL + Python
- If you want to change/add/extend something: "do it, just do it" and create pull request.

# Links
- [JQuery](https://jquery.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Calendar](https://github.com/fullcalendar/fullcalendar)
- [Arbor.js](https://github.com/samizdatco/arbor)
- [Timeline](https://github.com/CodyHouse/vertical-timeline)
- [Json2Html](https://github.com/wtf-develop/JSONtemplate)
- [JQueryUI](https://jqueryui.com/)
- [Icons](https://github.com/feathericons/feather)
