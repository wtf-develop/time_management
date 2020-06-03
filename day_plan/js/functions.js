function buildWebUI() {
    J2H.getJSON('api/get_day_plan.py', function(json) {
        if (isGoodResponse(json)) {
            $('#content').html(J2H.process(templates, 'task_card', json))

        }

    })
}