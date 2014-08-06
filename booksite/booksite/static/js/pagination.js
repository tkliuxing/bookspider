// filter and sort table.
$(function() {
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
    // ------- pagination --------
    $(".pagination a[data-num]").each(function(i, obj) {
        var page_num = $(obj).data("num");
        var url_obj = geturlqueryobj(location.href);
        url_obj["p"] = page_num;
        $(obj).attr("href", genurlquerystring(url_obj));
    });
    $("a.per-page").click(function() {
        var per_page = $(this).data("number");
        var url_obj = geturlqueryobj(location.href);
        url_obj["pp"] = per_page;
        url_obj["p"] = "0";
        location.href = genurlquerystring(url_obj);
        return false;
    });
    $("form.page").submit(function() {
        var page_num = $("form.page").find('input[name="p"]').val();
        var url_obj = geturlqueryobj(location.href);
        url_obj["p"] = page_num;
        location.href = genurlquerystring(url_obj);
        return false;
    });
    $("form.filter").submit(function() {
        var f = $("form.filter");
        var form_url = $("form.filter").attr("action");
        var f_url_obj = geturlqueryobj(f.serialize());
        var url_obj = geturlqueryobj(location.href);
        var i;
        for (i in f_url_obj) {
            url_obj[i] = f_url_obj[i]
        }
        if (url_obj.hasOwnProperty("p") == true) {
            url_obj["p"] = '';
        }
        if (url_obj.hasOwnProperty("s") == true) {
            url_obj["s"] = '';
        }
        location.href = form_url + genurlquerystring(url_obj);
        return false;
    });
    // ------- END pagination -------
    // ----- sort -----
    $("th>span[data-skey]").toggleClass("tha");
    $("th>span[data-skey]").click(function(event) {
        var this_span = $(event.target);
        var qobj = geturlqueryobj(location.href);
        qobj["s"] = this_span.data('skey');
        location.href = genurlquerystring(qobj);
    });
    var sort_key = urlparse('s');
    $("th>span[data-skey]").each(function(pos, obj) {
        // 根据排序关键字来添加图标
        if (encodeURI($(obj).data('skey')) == sort_key) {
            $(obj).parent().append("<span class='caret'></span>");
        }
    });
    if ($("th span.caret").length == 0) {
        // 如果没有默认的排序选项,则添加图标到节点编号列
        $("th").eq(1).append("<span class='caret'></span>");
    }
    // ----- end sort -----
});