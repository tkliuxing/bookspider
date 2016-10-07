from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BookAppConfig(AppConfig):
    name = 'book'
    verbose_name = _("看小说么主站")
