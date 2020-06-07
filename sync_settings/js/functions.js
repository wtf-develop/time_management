function buildWebUI() {
    J2H.getJSON('api/get_devices.py', function(json) {
        if (isGoodResponse(json)) {
            $('#content').html(J2H.process('page_structure', json))
            graph.init(json.data)
        }
    })
}