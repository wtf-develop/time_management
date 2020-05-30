#!/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/bin/python3
# !/usr/bin/env python3
import os, sys, inspect, cgitb

cgitb.enable()
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir)

from _common.api import auth
from _common.api import headers

#headers.htmlPage(True, "login/index.py")
headers.htmlPage(False)
print("""
<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="Reminder web application">
    <meta name="author" content="Arefev Leonid">
    <title>WEB-Reminder</title>
    <link href="_common/css/bootstrap.min.css" rel="stylesheet">
    <link href="_common/css/custom.css" rel="stylesheet">
</head>

<body>
    <div id="content">
        <div style="text-align:center;"><br />&nbsp;<br><img src="_common/img/loader.gif" /><br />&nbsp;&nbsp;Loading...</div>
    </div>

    <script type="text/javascript" src="_common/js/jquery.min.js"></script>
    <script type="text/javascript" src="_common/js/json2html.js"></script>
    <script type="text/javascript" src="_common/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="_common/js/feather.min.js"></script>
    <script type="text/javascript" src="main/js/functions.js"></script>

    <script type="text/javascript">
        var templates = {};

        function init() {
            //J2H.setTranslationArray(translates.en); // optional
            J2H.loadTemplatesArray(templates, ["main/html/navigation.html"], loadingCallback);
        }

        function loadingCallback() {
            $("#content").html(J2H.process(templates, "page_structure", {}));
            feather.replace()
            buildWebUI();
        }
        init(); //Run it immediately after loading page
    </script>
</body>

</html>
      """)
