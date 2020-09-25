function buildWebUI() {
    jth.getJSON('api/get_week_plan.py?devid=' + getDevId()+'&'+getTimezoneParameter(), function(json) {
        if (isGoodResponse(json)) {
            $('#content').injectJSON(json, 'page_structure')
            applyTimeline();
        }

    })
}