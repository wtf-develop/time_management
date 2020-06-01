# About

OpenSource personal time managment system. Server source code for [this Reminder application](https://play.google.com/store/apps/details?id=ru.mcsar.schedule) from GooglePlay

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
MySQL or MariaDB

# FAQ
- If you want to install it somewhere and don't know how to do this: Google can help you.
- If you want to change/add something: Do it byself and create merge request.
