$(function(){
	const messages = {
		nothingSelected: "Please select type of task."
	};

    $('.user-actions button').on('click', function(e){
        $('button.active').removeClass('active');
        $(this).addClass('active');
    });

    $('#next-step').on('click', function(e){
        if ($('.user-actions .option').hasClass('active')) {
        	$('#next-step').click();
        } else {
        	toast('<h6 class="white-color">' + messages.nothingSelected + '</h6>', 4000, 'rounded');
        }

        e.preventDefault();
    });
})