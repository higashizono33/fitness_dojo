function ajax_get_update()
{
    $.get(url, function(results){
        //get the parts of the result you want to update. Just select the needed parts of the response
        var eventTable = $("table", results);
        var page = $("#page_nav", results);
        //update the ajax_table_result with the return value
        $('#page_row').html(page);
        $('#event_table').html(eventTable);
    }, "html");
}

//bind the corresponding links in your document to the ajax get function
$(document).ready(function() {
    $('.pagination #prev').click(function(e){
        e.preventDefault();
        url = ($('.pagination #prev')[0].href);
        ajax_get_update();
    });
    $('.pagination .current').click(function(e){
        e.preventDefault();
        url = ($(this)[0].href);
        ajax_get_update();
    });
    $('.pagination #next').click(function(e){
        e.preventDefault();
        url = ($('.pagination #next')[0].href);
        ajax_get_update();
    });
});
//since the links are reloaded we have to bind the links again
//to the actions
$(document).ajaxStop(function(){
    $('.pagination #prev').click(function(e){
        e.preventDefault();
        url = ($('.pagination #prev')[0].href);
        ajax_get_update();
    });
    $('.pagination .current').click(function(e){
        e.preventDefault();
        url = ($(this)[0].href);
        ajax_get_update();
    });
    $('.pagination #next').click(function(e){
        e.preventDefault();
        url = ($('.pagination #next')[0].href);
        ajax_get_update();
    });
});