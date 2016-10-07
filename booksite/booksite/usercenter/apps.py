from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UserCenterAppConfig(AppConfig):
    name = 'usercenter'
    verbose_name = _("用户中心")
