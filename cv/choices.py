from django.utils.translation import gettext as _
from django.db import models


class JUNIOR_CERT_TEST_LEVEL(models.TextChoices):

    Common = ('Common')
    Higher = ('Higher')
    Ordinary = ('Ordinary')

class JUNIOR_CERT_TEST_RESULT(models.TextChoices):

    HIGHERMERIT = ('HIGHER MERIT')
    MERIT = ('MERIT')
    ACHIEVED = ('ACHIEVED')
    PARTIALLYACHIEVED = ('PARTIALLY ACHIEVED')
    NOTGRADED = ('NOT GRADED')

class LEAVING_CERT_TEST_RESULT(models.TextChoices):

    Pending = ('PENDING')
    H1 = ('H1')
    H2 = ('H2')
    H3 = ('H3')
    H4 = ('H4')
    H5 = ('H5')
    H6 = ('H6')
    H7 = ('H7')
    O1 = ('O1')
    O2 = ('O2')
    O3 = ('O3')
    O4 = ('O4')
    O5 = ('O5')
    O6 = ('O6')
    O7 = ('O7')

class LEAVING_CERT_TEST_LEVEL(models.TextChoices):

    Common = ('Common')
    Higher = ('Higher')
    Ordinary = ('Ordinary')

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


class SKILLS(models.TextChoices):
    SelfStarter= "1", _('SELF STARTER')
    PeopleSkills= "2", _('People Skills')
    CriticalThinkingSkills= "3", _('Critical Thinking Skills')
    PracticalSkills= "4", _('Practical Skills')
    CommunicationSkills= "5", _('Communication Skills')
    TeamworkSkills= "6", _('Teamwork Skills')
    InformationSkills= "7", _('Information Skills')
    CreativeSkills= "8", _('Creative Skills')
    CriticalProblemSolving= "9", _('Critical Problem Solving')


SKILLS_DESCRIPTIONS = {
    SKILLS.SelfStarter: "I take initiative and take on projects independently, I can work without supervision",
    SKILLS.PeopleSkills: "I am liked by others. I can interact, influence and communicate well with other people",
    SKILLS.CriticalThinkingSkills: "I can look at a situation, find the cause of the problem and then come up with a solution.",
    SKILLS.PracticalSkills: "I enjoy being physically involved in a project or task",
    SKILLS.CommunicationSkills:  "I can absorb, share and understand ideas or information. I can communicate well through written or spoken words",
    SKILLS.TeamworkSkills: "I enjoy working in a group of people to achieve a common aim",
    SKILLS.InformationSkills: "I use technology daily for sending messages, video calls, searching the internet, filing, cloud storage and social media on any device",
    SKILLS.CreativeSkills: "I can think about problems differently and can find interesting ways to approach tasks. I see things from a unique perspective",
    SKILLS.CriticalProblemSolving: "I have the ability to use knowledge, facts and data to effectively solve problems. I can think on my feet, assess problems and find solutions",
}

SKILLS_VALUED = {
    SKILLS.SelfStarter: "SELF STARTER",
    SKILLS.PeopleSkills: "People Skills",
    SKILLS.CriticalThinkingSkills: "Critical Thinking Skills",
    SKILLS.PracticalSkills: "Practical Skills",
    SKILLS.CommunicationSkills:  "Communication Skills",
    SKILLS.TeamworkSkills: "Teamwork Skills",
    SKILLS.InformationSkills: "Information Skills",
    SKILLS.CreativeSkills: "CreativeSkills",
    SKILLS.CriticalProblemSolving: "Critical Problem Solving",
}


class QUALITY(models.TextChoices):
    Intuitive= "1", _('Intuitive')
    Persistent= "2", _('Persistent')
    Enthusiastic= "3", _('Enthusiastic')
    Persuasive= "4", _('Persuasive')
    Empathic= "5", _('Empathic')
    Patient = "6", _('Patient')
    A_Good_Listener= "7", _('A_Good_Listener')
    Expressive= "8", _('Expressive')


QUALITY_DESCRIPTIONS = {
    QUALITY.Intuitive: "I have the ability to understand or know something by instinct.",
    QUALITY.Persistent: "I am determined to see projects through to the end. I don't give up easily.",
    QUALITY.Enthusiastic: "I have an active and motivated attitude. I get satisfaction from getting things done and pursuing my goals.",
    QUALITY.Persuasive: "I have the ability to persuade and help others see and agree with my point of view.",
    QUALITY.Empathic: "I have the ability to feel and understand what others need.",
    QUALITY.Patient: "I am able to behave calmly in the face of frustration or annoyance.",
    QUALITY.A_Good_Listener: "I can make others feel supported and can create a safe environment in which issues can be discussed.",
    QUALITY.Expressive: "I am positive, social, and generous. I enjoy being included."
}

QUALITY_VALUED = {
    QUALITY.Intuitive: 'Intuitive',
    QUALITY.Persistent: 'Persistent',
    QUALITY.Enthusiastic: 'Enthusiastic',
    QUALITY.Persuasive: 'Persuasive',
    QUALITY.Empathic: 'Empathic',
    QUALITY.Patient: 'Patient',
    QUALITY.A_Good_Listener: 'A_Good_Listener',
    QUALITY.Expressive:'Expressive',
}