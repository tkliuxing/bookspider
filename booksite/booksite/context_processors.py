# -*- coding: utf-8 -*-
from django.conf import settings
from booksite.book.models import KeyValueStorage, Book
from booksite.usercenter.models import BookMark


def analystics(request):
    context_extras = {}
    if hasattr(settings, 'BAIDUTONGJI_ID'):
        context_extras['BAIDUTONGJI_ID'] = settings.BAIDUTONGJI_ID
    if hasattr(settings, 'GA_ID'):
        context_extras['GA_ID'] = settings.BAIDUTONGJI_ID
    # if hasattr(settings, 'ZHANZHANGTONGJI_ID'):
    #     context_extras['ZHANZHANGTONGJI_ID'] = settings.BAIDUTONGJI_ID
    return context_extras


def categorys(request):
    CATEGORYS_KV, created = KeyValueStorage.objects.get_or_create(
        key='CATEGORYS',
        defaults={'value': '', 'long_value': ''}
    )
    if created:
        real_categorys = Book.objects.order_by('category').distinct('category').values_list('category', flat=True)
        CATEGORYS_KV.val = {chr(x[0]): x[1] for x in zip(range(97, 123), real_categorys)}
        CATEGORYS_KV.save()
    CATEGORYS = [{'name': x[1], 'key':x[0]} for x in CATEGORYS_KV.val.items()]
    return {'categorys': CATEGORYS}


def bookmark_update_count(request):
    if request.user.is_anonymous():
        return {}
    count = BookMark.objects.filter(user=request.user, update=True).count()
    return {'bookmark_update': count}
