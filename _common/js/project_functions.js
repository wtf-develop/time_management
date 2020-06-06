function isGoodResponse(json) {
    J2H.translate(json)
    if (json.error !== undefined && json.error.state !== undefined && json.error.state) {
        alert(json.error.title + "\n" + json.error.message); // replace to your own implementation
        return false;
    }
    return true;
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
    if (browserLang === undefined || browserLang == null) {
        return ""
    }
    return browserLang;
}


function showProgressIn(element, mainPage = false) {
    var temp = $(element).attr("oldhtml");
    if (temp === undefined) temp = '';
    if (temp.length > 0) return;
    temp = $(element).html();
    if (mainPage) {
        $(element).html('<img width=16 height=16 src="_common/img/loader.gif" />');
    } else {
        $(element).html('<img width=16 height=16 src="../_common/img/loader.gif" />');
    }
    $(element).attr("oldhtml", temp);
    $(element).attr("disabled", true);
}

function hideProgressIn(element) {
    var temp = $(element).attr("oldhtml") + '';
    if (temp === undefined) temp = '';
    if (temp.length < 1) return;
    $(element).html(temp);
    $(element).attr("oldhtml", '');
    $(element).removeAttr("disabled");
}