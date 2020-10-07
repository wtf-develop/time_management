#!/usr/local/bin/python3

import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(currentdir))
from _common.api import headers
from _common.api import auth
from _common.api import translation

auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
headers.htmlPage(False)

print("""<!DOCTYPE html>
<html lang='""" + auth.user_lang + """'>
<head>
    <meta charset="utf-8" />
    <title>""" + translation.getAppName(auth.user_lang) + """ - Android application</title>
    <meta name="description" content="The application will notify the user about various events. Widgets: Week, Colored Notes, Microphone, Calendar. Time and place reminder">
    <meta name="keywords" content="Reminder, Android, Time and Place, Запоминатор, Напоминалка, Напоминатор, MachEs!">
    <meta name="author" content="Arefev Leonid" />
    <meta name="referrer" content="no-referrer" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <link rel="icon" href="data:;base64,iVBORw0KGgo=" />
    <link href="../_common/css/bootstrap.min.css" rel="stylesheet" />
    <link href="../_common/css/custom.css" rel="stylesheet" />
    <link href="css/login.css" rel="stylesheet" />

</head>

<body>
    <div id="particles-js" style="position: absolute;left:0;top:0;">
        <canvas class="particles-js-canvas-el" style="width: 100%; height: 100%;" width="1829" height="429"></canvas>
    </div>
    <div id="content">
    </div>

    <script type="text/javascript" src="../_common/js/jquery.min.js"></script>
    <script type="text/javascript" src="../_common/js/json2html.min.js"></script>
    <script type="text/javascript" src="../_common/js/feather.min.js"></script>
    <script type="text/javascript" src="../_common/js/project_functions.js"></script>
    <script type="text/javascript" src="js/functions.js"></script>
    <script type="text/javascript" src="js/particles.min.js"></script>

<script type="text/javascript">
    var templates = {};

    function init() {
        setLanguage(getLang())
        $("#content").hide(); // optional
    }

    init(); //Run it immediately after loading page


    function setLanguage(selectedLang) {
        storeLang(selectedLang);
        jth.getJSON('api/get_login_translation.py',function(json){
            if(isGoodResponse(json)){
                jth.setTranslationArray(json.data.data);
                extLang=json.data.code;
                users_count=json.data.users_count;
                version=json.server.version;
                storeLang(extLang);
                jth.loadTemplatesArray( ["../_common/html/templates.html","html/templates.html"], buildWebUI);
            }else{
                jth.loadTemplatesArray( ["../_common/html/templates.html","html/templates.html"], buildWebUI);
            }
        });
        return selectedLang;
    }

    var extLang='en';
    var version='';
    var users_count=0;
    function buildWebUI() { //create all elements inside page (Structure of page)
        $("#content").injectJSON({code:extLang,version:version,users:users_count},"page");
        feather.replace();        
        $("#content").fadeIn(150);
    }


particlesJS.load('particles-js', 'js/particles-config.json', function() {});
</script>
</body>
</html>""")
