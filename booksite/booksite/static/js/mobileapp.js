(function($) {
	// using jQuery
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = $.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');

	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
		crossDomain: false, // obviates need for sameOrigin test
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type)) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});

	$.mobile.document.on("click", ".dnchange", function() {
		if (DATA_DIC.dn === 'day') {
			$("[data-theme='a']").attr('data-theme', 'b');
			$(".ui-page-theme-a").addClass("ui-page-theme-b");
			$(".ui-page-theme-a").removeClass("ui-page-theme-a");
			DATA_DIC.dn = 'night';
		} else {
			$("[data-theme='b']").attr('data-theme', 'a');
			$(".ui-page-theme-b").addClass("ui-page-theme-a");
			$(".ui-page-theme-b").removeClass("ui-page-theme-b");
			DATA_DIC.dn = 'day';
		}
	})

	// Login Form
	// $.mobile.document.on("submit", "#loginform", function() {
	// 	var data = $("#loginform").serializeArray();
	// 	var url = $("#loginform").attr('action');
	// 	$.post(url, data, function(data) {
	// 		if (data.success) {
	// 			console.log(data);
	// 			$.mobile.changePage(data.data.next);
	// 		} else {
	// 			$("#error_message").text("用户名或密码错误");
	// 		}
	// 	}, 'json');
	// 	return false;
	// })

	$.mobile.document.on("pagebeforeshow", "body", function() {
		//昼夜切换
		if (DATA_DIC.dn === 'day') {
			$("[data-theme='b']").attr('data-theme', 'a');
			$(".ui-page-theme-b").addClass("ui-page-theme-a");
			$(".ui-page-theme-b").removeClass("ui-page-theme-b");
		} else {
			$("[data-theme='a']").attr('data-theme', 'b');
			$(".ui-page-theme-a").addClass("ui-page-theme-b");
			$(".ui-page-theme-a").removeClass("ui-page-theme-a");
		}
		console.log(DATA_DIC);
	});

	$.mobile.document.on("swipeleft", ".pagecontent", function() {
		$.mobile.changePage($(".next_a").eq(0).attr('href'));
	});
	$.mobile.document.on("swiperight", ".pagecontent", function() {
		$.mobile.changePage($(".prev_a").eq(0).attr('href'));
	});

	// 添加书签
	$.mobile.document.on('click', '.bookmark', function(event) {
		var page_id = $(".bookmark").eq(0).data("pageid");
		$.post(DATA_DIC["add_bookmark_url"], {
			pageid: page_id
		}, function(data) {
			if (data.success) {
				$(".bookmark").toggleClass("ui-icon-star");
				$(".bookmark").toggleClass("ui-icon-check");
				setTimeout(function() {
					$(".bookmark").toggleClass("ui-icon-check");
					$(".bookmark").toggleClass("ui-icon-star");
				}, 3000);
			}
		}, 'json');
		return false;
	});
	// Delete bookmark
	$.mobile.document.on('click', ".delbma", function(event) {
		var this_a = $(event.target);
		$.post(this_a.data("url"), {}, function(data) {
			if (data.success) {
				this_a.parent().parent().slideUp().remove();
			}
		}, 'json');
		return false;
	});

	// tap
	$.mobile.document.on('vclick', '.pagecontent', function(event) {
		var window_width = parseInt(window.screen.availWidth);
		var click_x = parseInt(event.clientX);
		if (click_x < (window_width / 5 * 2)) {
			window.scrollTo(0, window.scrollY - window.innerHeight + 20);
		}
		if ((window_width / 5 * 2) < click_x && click_x < (window_width / 5 * 3)) {
			$(".ui-footer").toolbar("toggle");
		}
		if ((window_width / 5 * 3) < click_x) {
			window.scrollTo(0, window.scrollY + window.innerHeight - 20);
		}
	});

})(jQuery);