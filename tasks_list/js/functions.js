function buildWebUI() {
    J2H.getJSON('api/get_tasks_list.py', function(json) {
        if (isGoodResponse(json)) {
            $('#content').html(J2H.process('page_structure', json))
            initTODO(json);
        }
    })
}

function initTODO() {
    $("#datepicker").datepicker();
    $("#datepicker").datepicker("option", "dateFormat", "dd/mm/yy");

    $(".task-container").droppable();
    $(".todo-task").draggable({
        revert: "valid",
        revertDuration: 200
    });
    todo.init($('#content'));
}