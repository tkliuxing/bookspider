(function($) {
	// utils function
	function geturlqueryobj(url) {
		var paraString = url.substring(url.indexOf("?") + 1, url.length).split("&");
		var paraObj = {}
		for (i = 0; j = paraString[i]; i++) {
			paraObj[j.substring(0, j.indexOf("=")).toLowerCase()] = j.substring(j.indexOf("=") + 1, j.length);
		}
		delete(paraObj[""])
		return paraObj
	}

	function urlparse(paras) {
		var paraObj = geturlqueryobj(location.href)
		var returnValue = paraObj[paras.toLowerCase()];
		if (typeof(returnValue) == "undefined") {
			return "";
		} else {
			return returnValue;
		}
	}

	function genurlquerystring(obj) {
		var qs = "";
		for (val in obj) {
			qs = qs + val + "=" + obj[val] + "&";
		}
		qs = "?" + qs;
		return qs;
	}
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
			$.get("./?invert=1", function(data) {}, 'json');
		} else {
			$("[data-theme='a']").attr('data-theme', 'b');
			$(".ui-page-theme-a").addClass("ui-page-theme-b");
			$(".ui-page-theme-a").removeClass("ui-page-theme-a");
			$.get("./?invert=1", function(data) {}, 'json');
		}
		if (DATA_DIC.footer_hidden === true) {
			$(".ui-footer-fullscreen").toolbar("hide");
		}
	});

	$.mobile.document.on("swipeleft", ".pagecontent", function() {
		$(".next_a").last().click();
		return false;
	});
	$.mobile.document.on("swiperight", ".pagecontent", function() {
		$(".prev_a").last().click();
		return false;
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
	// 页面底部加载书籍列表
	$(window).on('scrollstop', function() {
		if ($("#search").length) {
			var tag = "#searchrel";
		} else {
			if ($("#home").length) {
				var tag = "#indexrel";
			} else {
				return false;
			}
		}
		var now = Date.now();
		if (!$(tag).data("timestap")) {
			$(tag).data("timestap", now);
		} else {
			if (now - parseInt($(tag).data("timestap")) < 600) {
				return false;
			}
		}
		var scrollTop = $(window).scrollTop();
		var scrollHeight = $(document).height();
		var windowHeight = $(window).height();
		if (scrollTop + windowHeight >= scrollHeight) {
			var current_page = parseInt($(tag).data("currpage"));
			var total_page = parseInt($(tag).data("pagetotal"));
			if (current_page < total_page) {
				console.log(Date.now());
				var next_page = current_page + 1;
				var data = {
					'p': next_page
				};
				if (urlparse('s')) {
					data['s'] = decodeURIComponent(urlparse('s'));
				}
				$.get($(tag).data("loadurl"), data, function(data) {
					if (data.success) {
						$(tag).append(data.data);
						$(".bookinfo").collapsible({
							iconpos: "right",
							mini: true
						});
						// $(".bookbtn").button();
					}
					$(tag).data("currpage", next_page);
					$(tag).data("timestap", now);
				}, 'json');
			}
		}
	})
	// tap
	$.mobile.document.on('vclick', '.pagecontent', function(event) {
		var window_width = parseInt(window.screen.availWidth);
		var click_x = parseInt(event.clientX);
		if (click_x < (window_width / 5 * 2)) {
			window.scrollTo(0, window.scrollY - window.innerHeight + 20);
			return false;
		}
		if ((window_width / 5 * 2) < click_x && click_x < (window_width / 5 * 3)) {
			$(".ui-footer-fullscreen").toolbar("toggle");
			if (DATA_DIC.footer_hidden === true) {
				DATA_DIC.footer_hidden = false;
			} else {
				DATA_DIC.footer_hidden = true;
			}
			return false;
		}
		if ((window_width / 5 * 3) < click_x) {
			window.scrollTo(0, window.scrollY + window.innerHeight - 20);
			return false;
		}
	});
	// 加载gzip文件
	var load_zip = function(elements){
		elements.each(function(index){
			var this_ele = $(this);
			$.get(this_ele.data('pageurl'), function(data){
				console.log(this_ele);
				$(data).prependTo(this_ele);
				this_ele.removeClass('noload');
			});
		});
	}
	load_zip($(".bookpage-content"));
})(jQuery);
