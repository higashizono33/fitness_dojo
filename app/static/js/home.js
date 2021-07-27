$(document).ready(function(){
    $('body').on('change', '.date_form', function(e){
        e.preventDefault();
        var eventId = $(this).attr('event');
        $.ajax({
            url: '/edit/date/event/'+eventId,
            type: 'post',
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            data: $(this).serialize(),
            dataType: 'json',
        })
    })
    $('body').on('change', '.starttime_form', function(e){
        e.preventDefault();
        var eventId = $(this).attr('event');
        $.ajax({
            url: '/edit/starttime/event/'+eventId,
            type: 'post',
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            data: $(this).serialize(),
            dataType: 'json',
        })
    })
})