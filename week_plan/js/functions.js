function buildWebUI() {
    jth.getJSON('api/get_week_plan.py?devid=' + getDevId()+'&'+getTimezoneParameter(), function(json) {
        if (isGoodResponse(json)) {
            $('#content').html(jth.process('page_structure', json))
            applyTimeline();
        }

    })
}