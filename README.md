# About

OpenSource time managment system.

# Requrements
Python 3.3+


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
