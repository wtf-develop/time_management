function storeLang(cvalue) {
    var d = new Date();
    d.setTime(d.getTime() + (365 * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = "lang=" + cvalue + ";" + expires + ";sameSite=strict; path=/";
}

function checkLogin(data) {
    showProgressIn($('#submit_login'));
    jth.postJSON('api/check_login.py', data, function(json) {
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

function togglePassVisible(){
    var x = document.getElementById("password");
    if (x.type == "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
    var y = $("#passLogo");
    if (x.type == "password"){
        y.attr('data-feather','eye')
    }else{
        y.attr('data-feather','eye-off')
    }
    feather.replace();
    return false;
}