function buildWebUI() {
    J2H.getJSON('api/get_tasks_list.py?devid=' + getDevId(), function(json) {
        if (isGoodResponse(json)) {
            $('#content').html(J2H.process('page_structure', json))
            initTODO(json);
        }
    })
}

function initTODO(json) {
    todo.init($('#content'), json);
}