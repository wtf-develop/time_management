function buildWebUI() {
    jth.getJSON('api/get_tasks_list.py?devid=' + getDevId(), function(json) {
        if (isGoodResponse(json)) {
            $('#content').html(jth.process('page_structure', json))
            initTODO(json);
        }
    })
}

function initTODO(json) {
    todo.init($('#content'), json);
}