# About

OpenSource self-hosted personal time management system. Server source code was created for [this Reminder application](https://play.google.com/store/apps/details?id=ru.mcsar.schedule) from GooglePlay

# Installation

1) Setup server environment (look "Server requirements")
2) Remove old source files if they exists
3) Open file **/_common/api/_settings.py** and change database credentials
4) Run script **/zzz_install_and_then_remove_it.sh** as files owner
5) Remove all files with name **zzz_install_and_then_remove_it**.* with any extensions

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

### Apache2
with CGI folder
```xml
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
### Database
Install MySQL >= 5.5 or MariaDB >= 5.5

And install recommended driver for Python
```bash
pip3 install PyMySQL
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
- [Calendar](https://github.com/fullcalendar/fullcalendar)
- [Arbor.js](https://github.com/samizdatco/arbor)
- [Timeline](https://github.com/CodyHouse/vertical-timeline)
- [Json2Html](https://github.com/wtf-develop/JSONtemplate)
- [JQueryUI](https://jqueryui.com/)
- [Icons](https://github.com/feathericons/feather)
