function buildWebUI() {
    //Nothing to do. Called from parent frame
}

function drawUI() {
    J2H.getJSON('api/get_devices.py?filter0=1&filter1=1&filter2=1&filter3=1&filterl=0&selected=0', function(json) {
        if (isGoodResponse(json)) {
            if ($('#viewport').length < 1) {
                $('#content').html(J2H.process('page_structure', json))
                graph.init(json.data, updateData)
                $('.toggles').bootstrapToggle();
                $('.toggles').change(toggles_func);
            } else {
                graph.merge(json.data)
            }

        }
    })
}

var ignore_toggle = false;
var toggles_func = function() {
    if (ignore_toggle) return;
    ignore_toggle = true;
    $('.toggles').bootstrapToggle('off', true);
    $(this).bootstrapToggle('on');
    updateData();
}


var updateTimer

function updateData() {
    clearTimeout(updateTimer)
    updateTimer = setTimeout(function() {
        ignore_toggle = false;
        var filter0 = 'filter0=' + (document.getElementById('inlineCheckbox0').checked ? '0' : '1')
        var filter1 = 'filter1=' + (document.getElementById('inlineCheckbox1').checked ? '0' : '1')
        var filter2 = 'filter2=' + (document.getElementById('inlineCheckbox2').checked ? '0' : '1')
        var filter3 = 'filter3=' + (document.getElementById('inlineCheckbox3').checked ? '0' : '1')
        var filterl = 'filterl=' + (document.getElementById('inlineCheckboxl').checked ? '0' : '1')
        J2H.getJSON('api/get_devices.py?' + filter0 + '&' + filter1 + '&' + filter2 + '&' + filter3 + '&' + filterl + '&selected=' + graph.getSelectedId(), function(json) {
            if (isGoodResponse(json)) {
                if (typeof(json.data.links.me) == 'undefined') {
                    $('#editor').hide()
                } else {
                    $('#editor').html(J2H.process('editor', json))
                    $('#editor').fadeIn(500)
                    $('.devs').bootstrapToggle();
                    //$('.devs').change(toggles_func);

                }

                graph.merge(json.data)
                graph.restartMoving()

            }
        })
    }, 500)
}