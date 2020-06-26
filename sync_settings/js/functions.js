function buildWebUI() {
    J2H.getJSON('api/get_devices.py', function(json) {
        if (isGoodResponse(json)) {
            if($('#viewport').length<1){
                $('#content').html(J2H.process('page_structure', json))
                graph.init(json.data)
            }else{
                graph.merge(json.data)
            }

        }
    })
}

function updateData(){
    var filter0='filter0='+(document.getElementById('inlineCheckbox0').checked?'0':'1')
    var filter1='filter1='+(document.getElementById('inlineCheckbox1').checked?'0':'1')
    var filter2='filter2='+(document.getElementById('inlineCheckbox2').checked?'0':'1')
    var filter3='filter3='+(document.getElementById('inlineCheckbox3').checked?'0':'1')
    var filterl='filterl='+(document.getElementById('inlineCheckboxl').checked?'0':'1')
    J2H.getJSON('api/get_devices.py?'+filter0+'&'+filter1+'&'+filter2+'&'+filter3+'&'+filterl+'&selected=0', function(json) {
        if (isGoodResponse(json)) {
                graph.merge(json.data)
        }
    })
}