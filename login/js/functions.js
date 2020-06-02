function storeLang(cvalue) {
    var d = new Date();
    d.setTime(d.getTime() + (365 * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = "lang=" + cvalue + ";" + expires+";path=/";
}

function getLang() {
    var name = "lang=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    var browserLang = navigator.language || navigator.userLanguage;
    if(browserLang===undefined || browserLang==null){
        return ""
    }
    return browserLang;
}




function checkLogin(data) {
    showProgressIn($('#submit_login'));
    J2H.postJSON('api/check_login.py',data,function (json){
        if(isGoodResponse(json)){
            if(json.accepted!==undefined){
                window.location.href = "../index.py"
            }
        }else{
            hideProgressIn($('#submit_login'));
        }
    })
     return false;
}
