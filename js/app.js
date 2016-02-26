$(document).ready(function(){
    $('#preview').click(event, function(){
        event.preventDefault()
        $.getJSON(
            '/preview',
            {text: $('#code_text').val(),
             language: $('#language').val()},
            function(data){
                $('#preview_img').html(data['tag'])
            })
    })
})
