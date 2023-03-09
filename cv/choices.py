from django.utils.translation import gettext as _
from django.db import models


class JUNIOR_CERT_TEST_LEVEL(models.TextChoices):

    Common = "1", _('Common')
    Higher = "2", _('Higher')
    Ordinary = "3", _('Ordinary')

class JUNIOR_CERT_TEST_RESULT(models.TextChoices):

    HIGHERMERIT = "1", _('HIGHER MERIT')
    MERIT = "2", _('MERIT')
    ACHIEVED = "3", _('ACHIEVED')
    PARTIALLYACHIEVED = "4", _('PARTIALLY ACHIEVED')
    NOTGRADED= "5", _('NOT GRADED')

class USER_TITLE(models.TextChoices):

    MR = "1", _('MR')
    MRS = "2", _('MRS')
    MS = "3", _('MS')


    
    
    


