function buildWebUI(){
        J2H.getJSON('main/api/base_info.py',function(json){
            if(isGoodResponse(json)){
                $("#content").html(J2H.process(templates, "page_structure", json));
                selectLeftMenu(json.some_state);
                feather.replace();
            }
        })
}


var selectedItem
function selectLeftMenu(indx){
        selectedItem=indx;
        $('.nav-link').removeClass('active');
        if(indx===undefined||indx==''){
            indx=0;
        }
        if($('#menuitem'+indx).length<1){
            indx=0;
        }
        $('#menuitem'+indx).addClass('active');
        return runMenuLink(indx);
}


function runMenuLink(indx){
       if(indx===undefined||indx==''){
            indx=0;
       }
       if($('#menuitem'+indx).length<1){
            indx=0;
       }
       selectedItem=indx;
       var url=$('#menuitem'+indx).attr('href');
       if(url===undefined) return false;
       $('#frame_content',window.document).attr('src',url);
       /*try {
           document.getElementById('menuitem'+indx).click();
       } catch (err) {
           $('#frame_content',window.document).attr('src',url);
       }*/
       return false;
}