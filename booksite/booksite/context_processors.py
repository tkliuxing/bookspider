# -*- coding: utf-8 -*-
from django.conf import settings

def analystics(request):
    context_extras = {}
    if hasattr(settings, 'BAIDUTONGJI_ID'):
        context_extras['BAIDUTONGJI_ID'] = settings.BAIDUTONGJI_ID
    if hasattr(settings, 'GA_ID'):
        context_extras['GA_ID'] = settings.BAIDUTONGJI_ID
    # if hasattr(settings, 'ZHANZHANGTONGJI_ID'):
    #     context_extras['ZHANZHANGTONGJI_ID'] = settings.BAIDUTONGJI_ID
    return context_extras
