function storeLang(cvalue) {
    var d = new Date();
    d.setTime(d.getTime() + (365 * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = "lang=" + cvalue + ";" + expires;
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



function setLanguage(selectedLang) {
        if ((selectedLang != "en") && (selectedLang != "ru") && (selectedLang != "de")) {
            selectedLang = "en";
        }
        storeLang(selectedLang);
        //J2H.setTranslationArray(translates.en); // optional
        J2H.loadTemplatesArray(templates, ["html/templates.html"], loadingCallback);
        return selectedLang;
}


function checkLogin() {
     return false;
}
