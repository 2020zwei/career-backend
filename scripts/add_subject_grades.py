from calculator.models import Subject, SubjectGrade, Level
from django.db import transaction

GRADES = [
    {'grade_level':'H1','level':1,'Points':100},
    {'grade_level':'H2','level':1,'Points':88},
    {'grade_level':'H3','level':1,'Points':77},
    {'grade_level':'H4','level':1,'Points':66},
    {'grade_level':'H5','level':1,'Points':56},
    {'grade_level':'H6','level':1,'Points':46},
    {'grade_level':'H7','level':1,'Points':37},
    {'grade_level':'H8','level':1,'Points':0},
    {'grade_level':'O1','level':2,'Points':56},
    {'grade_level':'O2','level':2,'Points':46},
    {'grade_level':'O3','level':2,'Points':37},
    {'grade_level':'O4','level':2,'Points':28},
    {'grade_level':'O5','level':2,'Points':20},
    {'grade_level':'O6','level':2,'Points':12},
    {'grade_level':'O7','level':2,'Points':0},
    {'grade_level':'O8','level':2,'Points':0},
]

records_added = 0
def add_data():
    try:
        with transaction.atomic():
            for subject_obj in Subject.objects.all().exclude(pk=22):
                for grade in GRADES:
                    level_obj = Level.objects.get(pk=grade['level'])
                    subject_grade_object = SubjectGrade.objects.create(subject=subject_obj, grade=grade['grade_level'], point=grade['Points'], level=level_obj)
                    print('record added',subject_grade_object.pk)
    except Exception as e:
        print(e)

