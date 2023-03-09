from django.db import models
from user.models import Student
from .choices import JUNIOR_CERT_TEST_LEVEL,JUNIOR_CERT_TEST_RESULT, JOB_TITLE
from django.contrib.postgres.fields import ArrayField

class CV(models.Model):
    user=models.ForeignKey(Student, on_delete=models.CASCADE,unique=True)
    objective=models.TextField(max_length=300)
    is_juniorcert_test=models.BooleanField(default=False)
    skills=ArrayField(models.CharField(max_length=200), blank=True)
    HobbiesandInterests=models.TextField(max_length=300)

class Education(models.Model):
    year=models.PositiveSmallIntegerField()
    school = models.CharField(max_length=50)
    examtaken=models.CharField(max_length=50)
    user=models.ForeignKey(Student, on_delete=models.CASCADE)

class JuniorCertTest(models.Model):
    subject = models.CharField(max_length=50)
    level=models.CharField(choices=JUNIOR_CERT_TEST_LEVEL.choices,max_length=1)
    result=models.CharField(choices=JUNIOR_CERT_TEST_RESULT.choices,max_length=1)
    user=models.ForeignKey(Student, on_delete=models.CASCADE)

class Experience(models.Model):
    startdate = models.DateField()
    enddate=models.DateField()
    jobtitle=models.CharField(choices=JOB_TITLE.choices,max_length=1)
    #position=models.CharField(max_length=50, null=True)
    company=models.CharField(max_length=50, null=True)
    city=models.CharField(max_length=50, null=True)
    country=models.CharField(max_length=50, null=True)
    description=models.TextField(max_length=300, null=True)
    user=models.ForeignKey(Student, on_delete=models.CASCADE)

class Reference(models.Model):
    contactnumber = models.CharField(max_length=30)
    position=models.CharField(max_length=50)
    contactemail=models.CharField(max_length=50)
    cv=models.ForeignKey(CV, on_delete=models.CASCADE)

class Skills(models.Model):
    skill=models.CharField(max_length=50, null=True)
    description=models.TextField(max_length=300)
    user=models.ForeignKey(Student,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="skills"

class Qualities(models.Model):
    quality=models.CharField(max_length=50, null=True)
    description=models.TextField(max_length=300)
    user=models.ForeignKey(Student,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="qualities"

    



