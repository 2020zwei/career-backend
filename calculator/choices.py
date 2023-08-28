from django.utils.translation import gettext as _
from django.db import models


class SUBJECT_LEVELS(models.TextChoices):

    HIGHER = "higher", _('Higher')
    ORDINARY = "ordinary", _('Ordinary')
    FOUNDATION = "foundation", _('Foundation')
    

