function buildWebUI() {
    window.scrollTo(0, 1);
    jth.getJSON('main/api/base_info.py', function(json) {
        if (isGoodResponse(json)) {
            jth.translate(json,['name'])
            $("#content").html(jth.process("page_structure", json));
            runMenuLink(json.data.some_state)
            selectLeftMenu(json.data.some_state);
            feather.replace();
            window.scrollTo(0, 1);
        }
    })
}


function storePageIndex(index) {
    var d = new Date();
    d.setTime(d.getTime() + (365 * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = "indx=" + index + ";" + expires + ";SameSite=Strict;path=/";
}


var selectedItem = 0
var currentDevId = 0

function setDevId(id) {
    if (inRefreshProcess) return false;
    currentDevId = parseInt(id);
    inRefreshProcess = true;
    $('#dropdev_all').html($('#dropdev' + id).html())
    $('.dropdev_items').removeClass('active');
    $('#dropdev' + id).addClass('active');
    showProgressIn($('#dropdev_all'), true);
    setTimeout(function() {
        inRefreshProcess = false;
        hideProgressIn($('#dropdev_all'));
        selectLeftMenu(selectedItem);
    }, 600);
    try {
        document.getElementById("frame_content").contentWindow.buildWebUI();
    } catch (e) {}
    return false;
}

function selectLeftMenu(indx) {
    selectedItem = indx;
    $('.nav-link').removeClass('active');
    if (indx === undefined || indx == '') {
        indx = 0;
    }
    if ($('#menuitem' + indx).length < 1) {
        indx = 0;
    }
    $('#menuitem' + indx).addClass('active');
    $('#sidebarMenu').removeClass('show');
    $('.navbar-toggler').addClass('collapsed');
    $('.navbar-toggler').attr('aria-expanded', false);
    storePageIndex(indx);
    return true;
}


function runMenuLink(indx) {
    if (indx === undefined || indx == '') {
        indx = 0;
    }
    if ($('#menuitem' + indx).length < 1) {
        indx = 0;
    }
    selectedItem = indx;
    var url = $('#menuitem' + indx).attr('href');
    if (url === undefined) return false;
    try {
        document.getElementById('menuitem' + indx).click();
    } catch (err) {
        $('#frame_content', window.document).attr('src', url);
    }
    return false;
}


function toggleFullScreen() {
    try {
        var doc = window.document;
        var docEl = doc.documentElement;

        var requestFullScreen = docEl.requestFullscreen || docEl.mozRequestFullScreen || docEl.webkitRequestFullScreen || docEl.msRequestFullscreen;
        var cancelFullScreen = doc.exitFullscreen || doc.mozCancelFullScreen || doc.webkitExitFullscreen || doc.msExitFullscreen;

        if (!doc.fullscreenElement && !doc.mozFullScreenElement && !doc.webkitFullscreenElement && !doc.msFullscreenElement) {
            requestFullScreen.call(docEl);
        } else {
            cancelFullScreen.call(doc);
        }
    } catch (ex) {}
    return false;
}

var inRefreshProcess = false;

function refreshChildUI() {
    if (inRefreshProcess) return false;
    inRefreshProcess = true;
    showProgressIn($('#refreshbtn'), true);
    setTimeout(function() {
        inRefreshProcess = false;
        hideProgressIn($('#refreshbtn'));
    }, 999);
    try {
        document.getElementById("frame_content").contentWindow.buildWebUI();
    } catch (e) {}
    return false;
}


function __mainDevId() {
    return currentDevId;
}