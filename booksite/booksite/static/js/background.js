(function($) {
	// 导航栏高亮
	var navid = $('#NAVID').data('nav');
	if (navid) {
		$(".lnav>ul>li").removeClass('active');
		$("#lnav-" + navid).addClass("active");
		$("#lnav-" + navid).parent().parent().addClass("active");
	}
})(jQuery);