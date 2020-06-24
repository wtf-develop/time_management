function buildWebUI() {
    J2H.getJSON('api/get_week_plan.py?devid=' + getDevId()+'&'+getTimezoneParameter(), function(json) {
        if (isGoodResponse(json)) {
            $('#content').html(J2H.process('page_structure', json))
            applyTimeline();
        }

    })
}