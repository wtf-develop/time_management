function buildWebUI() {
    J2H.getJSON('api/get_week_plan.py', function(json) {
        if (isGoodResponse(json)) {
            $('#content').html(J2H.process( 'page_structure', json))
            applyTimeline();
        }

    })
}