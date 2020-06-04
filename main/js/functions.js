function buildWebUI() {
    window.scrollTo(0, 1);
    J2H.getJSON('main/api/base_info.py', function(json) {
        if (isGoodResponse(json)) {
            $("#content").html(J2H.process(templates, "page_structure", json));
            runMenuLink(json.some_state)
            selectLeftMenu(json.some_state);
            feather.replace();
            window.scrollTo(0, 1);
            //toggleFullScreen();
        }
    })
}


var selectedItem

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
    $('#sidebarMenu').toggleClass('show');
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
}