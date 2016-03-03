$(document).ready(function(){
    $('#preview').click(event, function(){
        event.preventDefault()
        if($('#code_text').val()){
            $.getJSON(
                '/preview',
                {text: $('#code_text').val(),
                 language: $('#language').val(),
                 style: $('#style').val(),
                 line_numbers: $('#line_numbers:checked').length},
                function(data){
                    $('#preview_img').html(data['tag'])
                })
        }
    })
    $('#download').click(event, function(){
        event.preventDefault()
        if($('#code_text').val()){
            $('#code_form').attr('action', '/download')
            $('#code_form').submit()
            $('#code_form').attr('action', '/submit_form')
        }
    })
})
