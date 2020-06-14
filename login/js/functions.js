function storeLang(cvalue) {
    var d = new Date();
    d.setTime(d.getTime() + (365 * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = "lang=" + cvalue + ";" + expires + ";path=/";
}

function checkLogin(data) {
    showProgressIn($('#submit_login'));
    J2H.postJSON('api/check_login.py', data, function(json) {
        if (isGoodResponse(json)) {
            if (json.data.accepted !== undefined) {
                window.location.href = "../index.py"
            }
        } else {
            hideProgressIn($('#submit_login'));
        }
    })
    return false;
}