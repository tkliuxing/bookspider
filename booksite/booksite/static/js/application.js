(function($) {
	ALLOWKEY = true;
	LOADMORE = false;
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
	// 登录页面
	$("#id_captcha_1").addClass("form-control").css({
		width: '50%',
		display: 'inline-block'
	});
	if ($("#CAPTCHA")) {
		var new_a = $("<a href='javascript:;' class='recaptcha'></a>");
		$("#id_captcha_1").attr("placeholder", "点击图片刷新");
		$("#CAPTCHA>img").css({
			width: '29%',
			height: '42px',
		});
		new_a.append($("#CAPTCHA>img"));
		$("#CAPTCHA").prepend(new_a);
		$("#CAPTCHA>a.recaptcha").click(function(event) {
			$.get($("#CAPTCHA").data('url'), function(data) {
				$("#CAPTCHA>a>img").attr('src', data.image_url);
				$("#id_captcha_0").val(data.key);
			}, 'json');
			return false;
		});
	}
	// 按钮效果
	$('.input-group').on('focus', '.form-control', function() {
		$(this).closest('.input-group, .form-group').addClass('focus');
	}).on('blur', '.form-control', function() {
		$(this).closest('.input-group, .form-group').removeClass('focus');
	});
	// 导航栏高亮
	var navid = $('#NAVID').data('nav');
	if (navid) {
		$(".nav.navbar-nav.main>li").removeClass('active');
		$("#" + navid).addClass("active");
		$("#" + navid).parent().parent().addClass("active");
	}
	// 键盘翻页
	$(document).keydown(function(e) {
		if (ALLOWKEY && !LOADMORE) {
			var prev = $(".prev_page_a").eq(0).attr("href");
			var next = $(".next_page_a").eq(0).attr("href");
			switch (e.which) {
				case 37:
					location.href = prev;
					break;
				case 39:
					location.href = next;
					break;
			}
		}
	});
	// 双击滚动
	scroller = false;
	$(".pagecontent").dblclick(function() {
		position = window.scrollY;
		if (scroller) {
			clearInterval(scroller);
			scroller = false;
		} else {
			scroller = setInterval(function() {
				window.scrollTo(0, position);
				position += 1;
			}, 40);
		}
		return false;
	});
	// 判断夜间模式
	if (DATA_DIC["invert"] && DATA_DIC["is_page"]) {
		$('.inv').toggleClass('invert');
		$('.navbar').toggleClass('navbar-inverse');
		$('.btn').toggleClass('transparent_class');
		$('.panel.panel-default .btn').removeClass('transparent_class');
	}
	// 切换夜间模式
	$(".btn.invert").die().live('click', function() {
		$('.inv').toggleClass('invert');
		$('.navbar').toggleClass('navbar-inverse');
		$('.btn').toggleClass('transparent_class');
		$('.panel.panel-default .btn').removeClass('transparent_class');
		$.get("./?invert=1", function(data) {}, 'json');
		return false;
	});
	// 加载gzip文件
	var load_zip = function(elements){
		elements.each(function(index){
			var this_ele = $(this);
			$.get(this_ele.data('pageurl'), function(data){
				console.log(this_ele);
				$(data).appendTo(this_ele);
				this_ele.removeClass('noload');
			});
		});
	}
	load_zip($(".pagecontent.noload"));
	// 加载后续章节
	$(".readnall").die().live('click', function() {
		var this_a = $(event.currentTarget);
		var page_number = this_a.data('pn');
		$.ajax({
			type: 'get',
			cache: 'false',
			url: '/nallpage/' + page_number + '/',
			dataType: 'json',
			success: function(data) {
				if (data.success) {
					LOADMORE = true;
					$('.nextbox').remove();
					$('#FIELD').append($(data.data));
					$('.col-md-12.text-center.pagebutton').remove();
					auto_width_pg();
					$(".PGDOWN").click(function() {
						window.scrollTo(0, window.scrollY + window.innerHeight - 20);
					});
					$(".PGUP").click(function() {
						window.scrollTo(0, window.scrollY - window.innerHeight + 20);
					});
					load_zip($(".pagecontent.noload"));
				}
			},
			beforeSend: function() {
				var target = $('.nextbox').eq(0);
				$('.nextbox a').hide();
				var opts = {
					lines: 15,
					length: 23,
					width: 4,
					radius: 20,
					corners: 0,
					rotate: 9,
					trail: 77,
					speed: 1.0,
					direction: 1,
					shadow: false,
					color: '#58d68d'
				};
				target.spin(opts);
			}
		})
	});
	// 添加书签
	$(".TBMABtn").die().live('click', function(event) {
		var this_a = $(event.currentTarget);
		var page_number = this_a.data('pn');
		$.post(DATA_DIC["add_bookmark_url"], {
			pageid: page_number
		}, function(data) {
			if (data.success) {
				$('#TBMA' + page_number).slideDown();
				setTimeout(function() {
					$('#TBMA' + page_number).slideUp()
				}, 2000);
			} else {
				$('#TBMAERR' + page_number).text(data.error_message);
				$('#TBMAERR' + page_number).slideDown();
				setTimeout(function() {
					$('#TBMAERR' + page_number).slideUp()
				}, 5000);
			}
		}, 'json');
		return false;
	});
	// 触屏翻页
	function auto_width_pg() {
		content_width_haf = parseInt($(".pagecontent").width() / 2);
		$(".PGDOWN").css("left", content_width_haf + 15);
		$(".PGDOWN").css("width", content_width_haf + "px");
		$(".PGUP").css("width", content_width_haf + "px");
	};
	auto_width_pg();
	$(".PGDOWN").click(function() {
		window.scrollTo(0, window.scrollY + window.innerHeight - 20);
	});
	$(".PGUP").click(function() {
		window.scrollTo(0, window.scrollY - window.innerHeight + 20);
	});
	// 更新图片章节
	$(".pagefixpic").die().live('click', function(event) {
		var this_a = $(event.currentTarget);
		$.post(this_a.data('url'), {}, function(data) {
			if (data.success) {
				var alert_window = this_a.parent().parent().find(".alert");
				alert_window.slideDown();
				setTimeout(function() {
					alert_window.slideUp()
				}, 10000);
				check_page_fn = function() {
					$.get(this_a.data('churl'), function(data) {
						if (data.success) {
							if (data.data.status === 'DONE') {
								clearInterval(check_page);
								location.reload(true);
							}
						} else {
							clearInterval(check_page);
							alert(data.error_message);
						}
					}, 'json');
				}
				check_page = setInterval(check_page_fn, 1500);
				check_page_fn();
			} else {
				alert(data.error_message);
			}
		}, 'json');
		return false;
	});
	// 编辑段落内容
	if ($(".modal").length) {
		$(".pagecontent>p").die().live('click', function(event) {
			var this_p = $(event.currentTarget);
			$(".modal").modal('toggle');
			ALLOWKEY = false;
			$("#Lineedit").find("textarea").val(this_p.text());
			$(document.getElementsByName("linenum")).val(this_p.data("parnum"));
			$(document.getElementsByName("pagenum")).val(this_p.parent().data("pagenum"));
			$("#Lineedit").unbind('submit');
			$("#Lineedit").submit(function() {
				$.post($("#Lineedit").attr("action"), $("#Lineedit").serializeArray(), function(data) {
					if (data.success) {
						$("#Savelinedone").text("保存成功!");
						$("#Savelinedone").slideDown();
						setTimeout(function() {
							$("#Savelinedone").slideUp();
							$(".modal").modal('toggle');
							ALLOWKEY = true;
						}, 1000);
						var page_div = this_p.parent();
						page_div.find('p').remove();
						$(data.data).appendTo(page_div);
					} else {
						$("#Savelinedone").text(data.error_message);
						$("#Savelinedone").slideDown();
						setTimeout(function() {
							$("#Savelinedone").slideUp();
						}, 2000);
					}
				}, 'json');
				return false;
			});
			$("#Delline").die().live('click', function() {
				var post_url = this_p.parent().data("dellurl");
				$.post(post_url, {
					"ln": this_p.data("parnum")
				}, function(data) {
					if (data.success) {
						$("#Savelinedone").text("删除成功!");
						$("#Savelinedone").slideDown();
						setTimeout(function() {
							$("#Savelinedone").slideUp();
							$(".modal").modal('toggle');
							ALLOWKEY = true;
						}, 1000);
						var page_div = this_p.parent();
						page_div.find('p').remove();
						$(data.data).appendTo(page_div);
					} else {
						$("#Savelinedone").text(data.error_message);
						$("#Savelinedone").slideDown();
						setTimeout(function() {
							$("#Savelinedone").slideUp();
						}, 2000);
					}
				}, 'json');
			});
		});
		$("#Closemodal").die().live('click', function() {
			$(".modal").modal('toggle');
			ALLOWKEY = true;
		});
	}
})(jQuery);
