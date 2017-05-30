$(function(){
    $('.user-actions button').on('click', function(e){
        $('button.active').removeClass('active');
        $(this).addClass('active');
    });

    $('#next-step').on('click', function(e){
        var activeBtn = $('.user-actions button').hasClass('active') ? 
            $('#next-step').click() : $('.alert-warning').removeClass('hide');

        e.preventDefault();
    });
})