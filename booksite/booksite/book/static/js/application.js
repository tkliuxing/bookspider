(function($) {
	$('.input-group').on('focus', '.form-control', function() {
		$(this).closest('.input-group, .form-group').addClass('focus');
	}).on('blur', '.form-control', function() {
		$(this).closest('.input-group, .form-group').removeClass('focus');
	});
})(jQuery);