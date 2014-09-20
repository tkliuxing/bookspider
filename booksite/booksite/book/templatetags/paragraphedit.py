# -*- coding: utf-8 -*-
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
