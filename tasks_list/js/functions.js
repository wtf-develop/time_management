function buildWebUI() {
    jth.getJSON('api/get_tasks_list.py?devid=' + getDevId(), function(json) {
        if (isGoodResponse(json)) {
            $('#content').injectJSON(json,'page_structure')
            initTODO(json);
        }
    })
}

function initTODO(json) {
    todo.init($('#content'), json);
}