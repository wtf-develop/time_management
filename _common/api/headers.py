import sys
import datetime
from _common.api import auth


def htmlPage(check_auth: bool = True, fail_redirection: str = "../login/index.py"):
    if check_auth:
        if auth.access_levels == 0:
            redirectionPage(fail_redirection)
            sys.exit()
    today = datetime.date.today()
    print("Content-Type: text/html;charset=utf-8")
    print("Expires: Wed, 11 May 1983 17:30:00 GMT")
    print("Cache-Control: no-store, no-cache, must-revalidate")
    print("Cache-Control: post-check=0, pre-check=0")
    print("Last-Modified:", today.strftime("%a, %d %b %Y %H:%M:%S"), "GMT")
    print("Pragma: no-cache")
    print(auth.credentialsHeader())
    print("")


def jsonAPI(check_auth: bool = True):
    today = datetime.date.today()
    print("Content-type: application/json;charset=utf-8")
    print("Expires: Wed, 11 May 1983 17:30:00 GMT")
    print("Cache-Control: no-store, no-cache, must-revalidate")
    print("Cache-Control: post-check=0, pre-check=0")
    print("Last-Modified:", today.strftime("%a, %d %b %Y %H:%M:%S"), "GMT")
    print("Pragma: no-cache")
    print(auth.credentialsHeader())
    print("")
    if check_auth:
        if auth.access_levels == 0:
            print(
                '{"error":{"state":true,"code":401,"title":"Unauthorized","message":"Please open login page"}}')
            sys.exit()


def errorResponse(title: str, message: str = '', code: int = 0):
    print('{"error":{"state":true,"title": "' + title +
          '","message":"' + message + '","code":' + str(code) + '}}')
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
                            <link rel="icon" href="data:;base64,iVBORw0KGgo=">
                            <script type="text/javascript">
                                window.location.href = '""" + url + """'
                            </script>
                            </head><body>
                            <p>Please follow <a href='""" + url + """'>this link</a>.</p>
                        </body></html>""")
    sys.exit()
