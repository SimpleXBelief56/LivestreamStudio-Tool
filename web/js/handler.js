function requestParsedVersesJSON(){
    var parsedVersesArray = undefined;
    $.ajax({
        url: "/requestverses",
        type: "GET",
        dataType: "json",
        success: function(requestedData){
            parsedVersesArray = requestedData;
        }
    })
    return parsedVersesArray;
}




