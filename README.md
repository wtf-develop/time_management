# About

OpenSource self-hosted personal time management system. Server source code was created for [this Reminder application](https://play.google.com/store/apps/details?id=ru.mcsar.schedule) from GooglePlay

[Current link https://wtf-dev.ru/sync/](https://wtf-dev.ru/sync/)
But you can install this sources in any other place.

# Installation

1) Setup server environment (look "Server requirements")
2) Create database structure from file **zzz_database.sql**
3) Save the settings file (from 4) and remove old source files if they exists.
4) Open file **/_common/api/_settings.py** and change settings.
5) Run script **/zzz_run_once.sh** as files owner
6) Remove all files with name prefix **zzz_** and with any extensions

For update process please start from step 2

# Server requirements
- Linux
- MacOS
- Windows? Really?? Replace **#!/usr/local/bin/python3** in all \*.py scripts at the top of file.

Can be any old personal computer. Or any modern dedicated server. You can try to install it even directly to your mobile device or router, if you know how to do this and want to have fun.

### Python >= 3.5
Or higher. While development process version was v3.7
```bash
sudo apt-get install python3
```
Create a link to **python3** interpreter from this installation inside **/usr/local/bin/** folder. May be to **pip3** command also.

### Database
Install MySQL >= 5.5 or MariaDB >= 5.5
```bash
sudo apt-get install mariadb-server
```
And install recommended mysql client for Python
```bash
/usr/local/bin/python3 -m pip install PyMySQL
```

### Apache2
Must be with CGI folder (**mod_cgi** must be enabled)
```xml
AddDefaultCharset UTF-8
SetEnv PYTHONIOENCODING utf8

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
May be next code will solve some problems after update. This is not necessary and not recommended. Only if you see some cached content and can not clear internal browser cache.
```xml
<FilesMatch "\.(html|htm|js|css)$">
    FileETag None
    <IfModule mod_headers.c>
        Header unset ETag
        Header set Cache-Control "max-age=0, no-cache, no-store, must-revalidate"
        Header set Pragma "no-cache"
        Header set Expires "Wed, 11 May 1983 17:30:00 GMT"
    </IfModule>
</FilesMatch>
```

# FAQ
- If you want to install this project somewhere and don't know how to do this: there are a lot of examples in Google by request: Apache(CGI mode) + MySQL + Python
- If you want to change/add/extend something: "do it, just do it" and create pull request.

# For developers
Please set auto-format tool to ignore "E24, E402" - look **pycodestyle.ini** for examples. And follow current code structure.

# Links
- [PyMySQL](https://github.com/PyMySQL/PyMySQL)
- [JQuery](https://jquery.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Json2Html](https://github.com/wtf-develop/JSONtemplate)
- [Calendar](https://github.com/fullcalendar/fullcalendar)
- [Arbor.js](https://github.com/samizdatco/arbor)
- [Timeline](https://github.com/CodyHouse/vertical-timeline)
- [JQueryUI](https://jqueryui.com/)
- [Icons](https://github.com/feathericons/feather)
- [particles.js](https://github.com/VincentGarreau/particles.js/)
