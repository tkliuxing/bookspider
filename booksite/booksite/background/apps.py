from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BackgroundConfig(AppConfig):
    name = 'background'
    verbose_name = _("看小说么后台管理")
