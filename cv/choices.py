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

class LEAVING_CERT_TEST_RESULT(models.TextChoices):

    Pending = "1", ('PENDING')
    H1 = "2", _('H1')
    H2 = "3", _('H2')
    H3 = "4", _('H3')
    H4 = "5", _('H4')
    H5 = "6", _('H5')
    H6 = "7", _('H6')
    H7 = "8", _('H7')
    O1 = "9", _('O1')
    O2 = "10", _('O2')
    O3 = "11", _('O3')
    O4 = "12", _('O4')
    O5 = "13", _('O5')
    O6 = "14", _('O6')
    O7 = "15", _('O7')

class LEAVING_CERT_TEST_LEVEL(models.TextChoices):

    HIGHER = "1", _('HIGHER')
    ORDINARY = "2", _('ORDINARY')
    COMMON = "3", _('COMMON')

class SUBJECTS(models.TextChoices):

    English= "1", _('ENGLISH')
    Mathematics= "2", _('MATHEMATICS')
    Irish= "3", _('IRISH')
    Accounting= "4", _('ACCOUNTING')
    Agricultural_Economics= "5", ('AGRICULTURAL ECONOMICS')
    Agricultural_Science= "6", _('AGRICULTURAL SCIENCE')
    Ancient_Greek= "7", ('ANCIENT_GREEK')
    Applied_Mathematics= "8", ('APPLIED MATHEMATICS')
    Arabic= "9", _('ARABIC')
    Art= "10", _('ART')
    Biology= "11", _('BIOLOGY')
    Bulgarian= "12", _('BULGARIAN')
    Business= "13", _('BUSINESS')
    Chemistry= "14", _('CHEMISTRY')
    Classical_Studies= "15", ('CLASSICAL STUDIES')
    Construction_Studies= "16", _('CONSTRUCTION STUDIES')
    Czech= "17", _('CZECH')
    Danish= "18", _('DANISH')
    Design_Communication_Graphics= "19",('DESIGN & COMMUNICATION GRAPHICS')
    Dutch= "20", _('DUTCH')
    Economics= "21", _('ECONOMICS')
    Engineering= "22", ('ENGINEERING')
    Estonian= "23", _('ESTONIAN')
    Finnish= "24", ('FINNISH')
    French= "25", ('FRENCH')
    Geography= "26", ('GEOGRAPHY')
    German= "27", ('GERMAN')
    Hebrew_Studies= "28", ('HEBREW STUDIES')
    History= "29", ('HISTORY')
    Home_Economics= "30", ('HOME ECONOMICS')
    Hungarian= "31", _('HUNGARIAN')
    Italian= "32", _('ITALIAN')
    Japanese= "33", ('JAPANESE')
    Latin= "34", _('LATIN')
    Latvian= "35", ('LATVIAN')
    Link_Modules= "36", ('LINK MODULES')
    Lithuanian= "37", _('LITHUANIAN')
    Maltese= "38", _('MALTESE')
    Modern_Greek= "39", ('MODERN GREEK')
    Music= "40", ('MUSIC')
    Physics= "41", _('PHYSICS')
    Physics_Chemistry= "42", _('PHYSICS & CHEMISTRY')
    Polish= "43", _('POLISH')
    Politics_Society= "44", _('POLITICS & SOCIETY')
    Portuguese= "45", _('PORTUGESE')
    Religious_Education= "46", ('RELIGIOUS EDUCATION')
    Romanian= "47", _('ROMANIAN')
    Russian= "48", _('RUSSIAN')
    Slovakian= "49", _('SLOVAKIAN')
    Slovenian= "50", _('SLOVENIAN')
    Spanish= "51", _('SPANISH')
    Swedish= "52", _('SWEDISH')
    Technology= "53", _('TECHNOLOGY')



class USER_TITLE(models.TextChoices):

    MR = "1", _('MR')
    MRS = "2", _('MRS')
    MS = "3", _('MS')


    
    
class JOB_TITLE(models.TextChoices):
    Assistant = "1", _('ASSISTANT')
    WorkShadow = "2", _('WORK SHADOW')
    Other = "3", _('OTHER')

