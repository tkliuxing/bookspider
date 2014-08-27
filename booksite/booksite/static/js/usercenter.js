(function($) {
	$(".delbma").click(function(event) {
		var this_a = $(event.target);
		$.post(this_a.data("url"), {}, function(data) {
			if (data.success) {
				this_a.parent().parent().slideUp().remove();
				alert(data.data);
			} else {
				alert(data.error_message);
			}
		}, 'json');
		return false;
	});
})(jQuery);