from django.utils.translation import gettext as _
from django.db import models


class DAY_OF_THE_WEEK(models.TextChoices):

    MONDAY = "1", _('Monday')
    TUESDAY = "2", _('Tuesday')
    WEDNESDAY = "3", _('Wednesday')
    THURSDAY = "4", _('Thursday')
    FRIDAY = "5", _('Friday')
    SATURDAY = "6", _('Saturday')
    SUNDAY = "7", _('Sunday')


