#!/usr/local/bin/python3

import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(currentdir))
from _common.api import auth
from _common.api import headers
from _common.api import translation

headers.htmlPage()

print("""<!DOCTYPE html>
<html lang='""" + auth.user_lang + """'>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <meta name="description" content="Reminder web application" />
    <meta name="author" content="Arefev Leonid" />
    <title>""" + translation.getAppName(auth.user_lang) + """: Week</title>
    <link rel="icon" href="data:;base64,iVBORw0KGgo=" />
    <meta name="referrer" content="no-referrer" />
    <link href="css/timeline.css" rel="stylesheet" />
    <link href="../_common/css/bootstrap.min.css" rel="stylesheet" />
    <link href="../_common/css/custom.css" rel="stylesheet" />


</head>

<body>
    <div id="content" class="pt-0 pl-2 pr-2">
        <div style="text-align:center;"><br />&nbsp;<br><img src="../_common/img/loader.gif" /><br />&nbsp;&nbsp;Loading...</div>
    </div>

    <script type="text/javascript" src="../_common/js/jquery.min.js"></script>
    <script type="text/javascript" src="../_common/js/json2html.js"></script>
    <script type="text/javascript" src="../_common/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="../_common/js/feather.min.js"></script>
    <script type="text/javascript" src="../_common/js/project_functions.js"></script>
    <script type="text/javascript" src="js/functions.js"></script>
    <script type="text/javascript" src="js/timeline.js"></script>

    <script type="text/javascript">
        var templates = {};

        function init() {
            J2H.setTranslationArray(""" + translation.get_array(auth.user_lang) + """); // optional
            J2H.loadTemplatesArray( ["../_common/html/templates.html", "html/templates.html", "html/timeline.html"], loadingCallback);
        }

        function loadingCallback() {
            buildWebUI();
        }
        init();
    </script>
</body>

</html>""")
