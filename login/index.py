#!/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/bin/python3
#!/usr/bin/env python3
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(currentdir)) #one level up "os.path.dirname()"

from _common.api import auth
from _common.api import headers


auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
headers.htmlPage(False)

print("""<!DOCTYPE html>
<html lang='"""+auth.user_lang+"""'>
<head>
    <title>Time and Place reminder application - WEB Login page</title>
    <meta name="description" content="The application will notify the user about various events. By place - location based reminder. Reminder by time. List for the day (simple todo). List without date (colored notes). Countdown (short intervals). Widgets: Today, Colored Notes, Microphone, Calendar. Sync timers and tasks (notes) with Google Calendar and Google Tasks">
    <meta name="keywords" content="Reminder, Android, Time and Place, Запоминатор, Напоминалка, Напоминатор">
    <meta name="author" content="Arefev Leonid">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <link rel="icon" href="data:;base64,iVBORw0KGgo=">
    <link href="../_common/css/bootstrap.min.css" rel="stylesheet">
    <link href="../_common/css/custom.css" rel="stylesheet">
    <link href="css/login.css" rel="stylesheet">

</head>

<body>
    <div id="content">
    </div>
    <script type="text/javascript" src="../_common/js/jquery.min.js"></script>
    <script type="text/javascript" src="../_common/js/json2html.js"></script>
    <script type="text/javascript" src="../_common/js/project_functions.js"></script>
    <script type="text/javascript" src="js/functions.js"></script>    

<script type="text/javascript">
    var templates = {};

    function init() {
        setLanguage(getLang())
        $("#content").hide(); // optional
    }

    init(); //Run it immediately after loading page


    function setLanguage(selectedLang) {
        storeLang(selectedLang);
        J2H.getJSON('api/get_login_translation.py',function(json){
            if(isGoodResponse(json)){
                J2H.setTranslationArray(json.data);
                extLang=json.code;
                storeLang(extLang);
                J2H.loadTemplatesArray(templates, ["html/templates.html"], buildWebUI);
            }else{
                J2H.loadTemplatesArray(templates, ["html/templates.html"], buildWebUI);
            }        
        });
        return selectedLang;
    }

    var extLang='en';
    function buildWebUI() { //create all elements inside page (Structure of page)
        $("#content").html(J2H.process(templates,"page",{code:extLang}));
        $("#content").fadeIn(150);
    }

</script>
</body>
</html>""")
