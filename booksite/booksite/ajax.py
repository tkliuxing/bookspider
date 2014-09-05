#-*- coding: utf-8 -*-
"""
AJAX返回值统一处理
返回统一格式的JSON数据
已封装为HttpResponse对象
"""
import simplejson as json
from django.http import HttpResponse

def must_ajax(func):
    def view(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponse(status=400)
        return func(request, *args, **kwargs)
    return view

def ajax_success(data=None, **kwargs):
    """
    返回请求成功的JSON数据
    由返回JSON的success:true来报告后端操作成功.
    返回的数据本身在JSON的data中.
    参数:
        data: 要返回的数据,只能由基本类型构成
        kwargs: 当data为空时,使用关键字变参来填充数据
    """
    if data is None:
        data = kwargs
    return_json = json.dumps({"data": data, "success": True})
    response = HttpResponse(return_json, mimetype="text/json")
    response['Cache-Control'] = 'no-cache'
    return response


def ajax_error(error_message, data=None, **kwargs):
    """
    返回请求成功的JSON数据
    由返回JSON的success:false来报告后端操作错误.
    参数必须有error_message,说明错误信息.
    返回的数据本身在JSON的data中.
    参数:
        error_message: 错误信息字符串,必填
        data: 要返回的数据,只能由基本类型构成
        kwargs: 当data为空时,使用关键字变参来填充数据
    """
    if data is None:
        data = kwargs or None
    if data:
        return_json = json.dumps({
            "data": data,
            "success": False,
            "error_message": error_message,
        })
    else:
        return_json = json.dumps({
            "success": False,
            "error_message": error_message,
        })
    response =  HttpResponse(return_json, mimetype="text/json")
    response['Cache-Control'] = 'no-cache'
    return response
