(function($) {
	$('.input-group').on('focus', '.form-control', function() {
		$(this).closest('.input-group, .form-group').addClass('focus');
	}).on('blur', '.form-control', function() {
		$(this).closest('.input-group, .form-group').removeClass('focus');
	});
	var navid = $('#NAVID').data('nav');
	if(navid){
		$(".nav.navbar-nav.main>li").removeClass('active');
		$("#" + navid).addClass("active");
		$("#" + navid).parent().parent().addClass("active");
	}
})(jQuery);