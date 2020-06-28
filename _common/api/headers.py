import datetime
import gzip
import json
import sys
import time

from _common.api import _settings
from _common.api import auth
from _common.api import utils


def htmlPage(check_auth: bool = True, fail_redirection: str = "../login/index.py"):
    if check_auth:
        if auth.access_levels == 0:
            redirectionPage(fail_redirection)
            sys.exit()
    today = datetime.datetime.now()
    print("Content-Type: text/html;charset=utf-8")
    print("Expires: Wed, 11 May 1983 17:30:00 GMT")
    print("Cache-Control: no-store, no-cache, must-revalidate")
    # print("Cache-Control: post-check=0, pre-check=0")
    print("Last-Modified:", today.strftime("%a, %d %b %Y %H:%M:%S"), "GMT")
    print("Pragma: no-cache")
    if not auth.isMobile:
        print(auth.credentialsHeader())

    print("")


def jsonAPI(check_auth: bool = True):
    today = datetime.datetime.now()
    if _settings.enable_gzip:
        sys.stdout.write("Content-type: application/json;charset=utf-8\r\n")
        sys.stdout.write("Expires: Wed, 11 May 1983 17:30:00 GMT\r\n")
        sys.stdout.write("Cache-Control: no-store, no-cache, must-revalidate\r\n")
        # sys.stdout.write("Cache-Control: post-check=0, pre-check=0\r\n")
        sys.stdout.write("Last-Modified: " + today.strftime("%a, %d %b %Y %H:%M:%S") + " GMT\r\n")
        sys.stdout.write("Pragma: no-cache\r\n")
        if not auth.isMobile:
            sys.stdout.write(auth.credentialsHeader() + "\r\n")

        sys.stdout.write('Content-Encoding: gzip\r\n\r\n')
        sys.stdout.flush()
        if check_auth:
            if auth.access_levels == 0:
                sys.stdout.buffer.write(__compress_string(
                        '{"error":{"state":true,"code":401,"title":"Login session failed",' +
                        '"message":"Please open login page"}}'))
                sys.exit()
    else:
        print("Content-type: application/json;charset=utf-8")
        print("Expires: Wed, 11 May 1983 17:30:00 GMT")
        print("Cache-Control: no-store, no-cache, must-revalidate")
        # print("Cache-Control: post-check=0, pre-check=0")
        print("Last-Modified:", today.strftime("%a, %d %b %Y %H:%M:%S"), "GMT")
        print("Pragma: no-cache")
        if not auth.isMobile:
            print(auth.credentialsHeader())
        print("")
        if check_auth:
            if auth.access_levels == 0:
                print(
                        '{"error":{"state":true,"code":401,"title":"Login session failed",' +
                        '"message":"Please open login page"}}')
                sys.exit()


def __compress_string(s: str):
    return gzip.compress(s.encode('utf-8'))


def errorResponse(message: str, title: str = '@str.error', code: int = 0):
    obj = {
        'error': {
            'state': True,
            'title': title,
            'message': message,
            'code': code
        }
    }
    if _settings.enable_gzip:
        sys.stdout.buffer.write(__compress_string(json.dumps(obj)))
    else:
        print(json.dumps(obj))
    sys.exit()


def __addInfoResponse(message: str, attachTo: dict, title: str = '') -> dict:
    attachTo['toast'] = {
        'state': True,
        'title': title,
        'message': message
    }
    return attachTo


def goodResponse(outputData: dict, toastMessage: str = None, toastTitle: str = None):
    toffset = time.timezone
    if time.daylight != 0:
        toffset = toffset - 3600
    server_info = {
        'timestamp': int(time.time()),
        'timezone': time.timezone,
        'dst': time.daylight,
        'timeoffset': toffset,
        # 'isotime': datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(),
        'info': datetime.datetime.now().timetuple(),
        'version': utils.getServerVersion()
    }
    if auth.isMobile:
        server_info['token'] = auth.credentials

    obj = {'server': server_info, 'data': outputData}
    if (toastMessage is not None) and (len(toastMessage) > 0):
        if (toastTitle is not None):
            obj = __addInfoResponse(toastMessage, obj, toastTitle)
        else:
            obj = __addInfoResponse(toastMessage, obj)
    if _settings.enable_gzip:
        sys.stdout.buffer.write(__compress_string(json.dumps(obj)))
    else:
        print(json.dumps(obj))
    sys.exit()


def redirectionPage(url: str):
    url = url.strip()
    print("Content-Type: text/html;charset=utf-8")
    print("Cache-Control: no-store, no-cache, must-revalidate")
    print("Location: " + url)
    print("")
    print("""<!DOCTYPE html><html>
             <head>
             <meta http-equiv="Refresh" content="0;url='""" + url + """'" />
             <link rel="icon" href="data:;base64,iVBORw0KGgo=" />
             <script type="text/javascript">
                 window.location.href = '""" + url + """'
             </script>
             </head><body>
             <p>Please follow <a href='""" + url + """'>this link</a>.</p>
             </body></html>""")
    sys.exit()
