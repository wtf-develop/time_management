function isGoodResponse(json) {
    J2H.translate(json)
    if (json.error !== undefined && json.error.state !== undefined && json.error.state) {
        alert(json.error.title + "\n" + json.error.message); // replace to your own implementation
        return false;
    }
    return true;
}


function showProgressIn(element) {
    var temp=$(element).html();
    $(element).html('<img width=16 height=16 src="../_common/img/loader.gif" />');
    $(element).attr("old",temp);
    $(element).attr("disabled",true);
}

function hideProgressIn(element) {
    var temp=$(element).attr("old");
    if(temp.length<1)return;
    $(element).html(temp);
    $(element).attr("old",'');
    $(element).removeAttr("disabled");
}