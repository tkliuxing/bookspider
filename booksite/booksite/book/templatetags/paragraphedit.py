# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils import six
from django.utils.functional import allow_lazy
from django.utils.html import escape
from django.utils.text import normalize_newlines
from django.utils.safestring import mark_safe, SafeData


register = Library()


def linebreaks(value, autoescape=False):
    """Converts newlines into <p> and <br />s."""
    value = normalize_newlines(value)
    paras = re.split('\n{2,}', value)
    if autoescape:
        paras = ['<p data-parnum="%s">%s</p>' % (i, escape(p).replace('\n', '<br />')) for i, p in enumerate(paras)]
    else:
        paras = ['<p data-parnum="%s">%s</p>' % (i, p.replace('\n', '<br />')) for i, p in enumerate(paras)]
    return '\n\n'.join(paras)
linebreaks = allow_lazy(linebreaks, six.text_type)


@register.filter("paragraphlines", is_safe=True, needs_autoescape=True)
@stringfilter
def paragraphlines_filter(value, autoescape=None):
    """
    Replaces line breaks in plain text with appropriate HTML; a single
    newline becomes an HTML line break (``<br />``) and a new line
    followed by a blank line becomes a paragraph break (``</p>``).
    """
    autoescape = autoescape and not isinstance(value, SafeData)
    return mark_safe(linebreaks(value, autoescape))

@register.filter("numtocny", is_safe=True)
@stringfilter
def numtocny(data):
    return numtocn(data, cny=True)

@register.filter("numtocnnum", is_safe=True)
@stringfilter
def numtocnnum(data):
    return numtocn(data, cny=False)


def numtocn(data, cny=True):
    """
    算法说明：要求字符串输入，现将字符串差费为整数部分和小数部分生成list[整数部分,小数部分]
    将整数部分拆分为：[亿，万，仟]三组字符串组成的List:['0000','0000','0000']（根据实际输入生成阶梯List）
    例如：600190000010.70整数部分拆分为：['600','1900','0010']
    然后对list中每个字符串分组进行大写化再合并
    最后处理小数部分的大写化
    """
    cdict = {1: '', 2: '拾', 3: '佰', 4: '仟'} if cny else {1: '', 2: '十', 3: '百', 4: '千'}
    xdict = {2: '万', 3: '亿', 4: '兆'}
    xdict[1] = '元' if cny else ''
    if cny:
        gdict = {'0': '零', '1': '壹', '2': '贰', '3': '叁','4': '肆',
        '5': '伍', '6': '陆', '7': '柒', '8': '捌', '9': '玖'}
    else:
        gdict = {'0': '零', '1': '一', '2': '二', '3': '三', '4': '四',
        '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'}
    cdata = str(data).split('.')
    integer = ''.join(list(reversed(cdata[0])))
    decimal = cdata[1] if len(cdata) == 2 else []
    ch_str = ''
    # 分解字符数组[亿，万，仟]三组List:['0000','0000','0000']
    split_integer = list(
        reversed([''.join(list(reversed(integer[i:i+4])))
            for i in range(0,len(integer),4)])
    )
    split_integer_len = len(split_integer)  # 获取拆分后的List长度
    # 大写合并
    for i in range(split_integer_len):
        split_integer_group = split_integer[i]
        grouped_str = ''
        # 对[亿，万，仟]的list中每个字符串分组进行大写化再合并
        split_integer_group_len = len(split_integer_group)
        lk = split_integer_group_len
        for j in range(split_integer_group_len):
            this_char = split_integer_group[j]
            if this_char == '0':
                if j < split_integer_group_len-1:
                    if split_integer_group[j+1] != '0':
                        grouped_str = grouped_str+gdict[this_char]
            else:
                grouped_str = grouped_str+gdict[this_char]+cdict[lk]
            lk -= 1
        if grouped_str == '':  # 有可能一个字符串全是0的情况
            ch_str += grouped_str  # 此时不需要将数字标识符引入
        else:
            # 合并：前字符串大写+当前字符串大写+标识符
            ch_str += grouped_str+xdict[split_integer_len-i]
    # 处理小数部分
    decimal_len = len(decimal)
    if cny:
        if decimal_len == 0:
            ch_str += '整'
        elif decimal_len == 1:  # 若小数只有1位
            if int(decimal[0]) == 0:
                ch_str += '整'
            else:
                ch_str += gdict[decimal[0]]+'角整'
        else:  # 若小数有两位的四种情况
            if int(decimal[0]) == 0 and int(decimal[1]) != 0:
                ch_str += '零'+gdict[decimal[1]]+'分'
            elif int(decimal[0]) == 0 and int(decimal[1]) == 0:
                ch_str += '整'
            elif int(decimal[0]) != 0 and int(decimal[1]) != 0:
                ch_str += gdict[decimal[0]]+'角'+gdict[decimal[1]]+'分'
            else:
                ch_str += gdict[decimal[0]]+'角整'
    else:
        if decimal_len != 0:
            ch_str = ch_str + '点'
            for decimal_char in decimal:
                ch_str += gdict[decimal_char]
    return ch_str
