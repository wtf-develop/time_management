function buildWebUI(){
        J2H.getJSON('main/api/base_info.py',function(json){
            if(isGoodResponse(json)){
                $("#content").html(J2H.process(templates, "page_structure", json));
                feather.replace()
            }
        })

}