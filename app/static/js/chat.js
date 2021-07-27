$(document).ready(function(){
    $('#form_message').on('submit', function(e){
        e.preventDefault();
        var groupId = $(this).attr('group');
        var eventId = $(this).attr('event');
        $.ajax({
            url: '/activity/group/'+groupId+'/event/'+eventId,
            type: 'post',
            data: $(this).serialize(),
            dataType: 'json',
            success: function(res){
                if(res.error){
                    $('.m_error').html('*'+res.error)
                } else {
                    $('#message_area').html(res.html);
                    $('#text_message').val('');
                    $('.m_error').html('');
                }
            }
        })
    })
    $('body').on('change', '.text_comment', function(e){
        e.preventDefault();
        var messageId = $(this).attr('message');
        $.ajax({
            url: '/comment/'+messageId,
            type: 'post',
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            data: $(this).serialize(),
            dataType: 'json',
            success: function(res){
                if(res.error){
                    $('.c_error').html('*'+res.error)
                } else {
                    $('#message_area').html(res.html);
                    $('#text_comment').val('');
                    $('.c_error').html('');
                }
            }
        })
    })
})