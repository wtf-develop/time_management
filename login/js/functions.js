function setCookie(cname, cvalue, exdays, path) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=" + path;
}

function getCookie(cname) {
    var name = cname + "=";
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
    return "";
}



function setLanguage(selectedLang) {
        if ((selectedLang != "en") && (selectedLang != "es") && (selectedLang != "ru") && (selectedLang != "fr") && (selectedLang != "de")) {
            selectedLang = "en";
        }
        setCookie('lang', selectedLang, 365, "/example/");
        J2H.setTranslationArray(translates[selectedLang])
        J2H.loadTemplatesArray(templates, ["html/templates.html"], function() {
            J2H.getJSON("api/response.json", function(json) { //change only some parts of page
                if (isGoodResponse(json)) {
                    $('#headerContainer').html(J2H.process(templates, "header", json));
                    $('#logoContainer').html(J2H.process(templates, "logo", json));
                    $('#formContainer').html(J2H.process(templates, "form", json));
                    $('#content').fadeIn(50);
                }
            })

        })
        return selectedLang;
}


function checkLogin() {
     return false;
}
