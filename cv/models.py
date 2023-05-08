from django.db import models
from users.models import Student
from .choices import JUNIOR_CERT_TEST_LEVEL,JUNIOR_CERT_TEST_RESULT, JOB_TITLE,USER_TITLE,SUBJECTS,LEAVING_CERT_TEST_LEVEL,LEAVING_CERT_TEST_RESULT
from django.contrib.postgres.fields import ArrayField

class CV(models.Model):
    user=models.ForeignKey(Student, on_delete=models.CASCADE)
    objective=models.TextField(max_length=300)
    is_juniorcert_test=models.BooleanField(default=False)
    skills=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    HobbiesandInterests=models.TextField(max_length=300,null=True)
    full_name = models.CharField(max_length=100, null=True)
    school =  models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=50, blank=True,null=True)
    town = models.CharField(max_length=50, blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    address2 = models.TextField(blank=True,null=True)
    eircode=models.CharField(max_length=7,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)


    def __str__(self):
        return self.user.full_name
       

class Education(models.Model):
    year=models.PositiveSmallIntegerField()
    school = models.CharField(max_length=50)
    examtaken=models.CharField(max_length=50)
    user=models.ForeignKey(Student, on_delete=models.CASCADE)

class JuniorCertTest(models.Model):
    subject = models.CharField(choices=SUBJECTS.choices,max_length=2)
    level=models.CharField(choices=JUNIOR_CERT_TEST_LEVEL.choices,max_length=2)
    result=models.CharField(choices=JUNIOR_CERT_TEST_RESULT.choices,max_length=2)
    user=models.ForeignKey(Student, on_delete=models.CASCADE)

class LeavingCertTest(models.Model):
    subject = models.CharField(choices=SUBJECTS.choices,max_length=2)
    level=models.CharField(choices=LEAVING_CERT_TEST_LEVEL.choices,max_length=2)
    result=models.CharField(choices=LEAVING_CERT_TEST_RESULT.choices,max_length=2)
    user=models.ForeignKey(Student, on_delete=models.CASCADE)

class Experience(models.Model):
    startdate = models.DateField()
    enddate=models.DateField()
    jobtitle=models.CharField(choices=JOB_TITLE.choices,max_length=1)
    company=models.CharField(max_length=50, null=True)
    city=models.CharField(max_length=50, null=True)
    country=models.CharField(max_length=50, null=True)
    description=models.TextField(max_length=300, null=True)
    is_current_work=models.BooleanField(default=False)
    user=models.ForeignKey(Student, on_delete=models.CASCADE)


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
    
class JobTitle(models.Model):
    title=models.CharField(max_length=60)
    def __str__(self):
        """return name of Job-Title"""
        return self.title
        
    
class Reference(models.Model):
    user_title=models.CharField(choices=USER_TITLE.choices,max_length=1,null=True)
    job_title=models.ForeignKey('JobTitle',null=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=True,blank=True)
    contact_number = models.CharField(max_length=30,null=True,blank=True)
    email=models.CharField(max_length=50,null=True,blank=True)
    organization_address=models.CharField(max_length=50,null=True,blank=True)
    area_code=models.IntegerField(null=True,blank=True)
    cv=models.ForeignKey(CV, on_delete=models.CASCADE)
    position=models.CharField(max_length=50,null=True,blank=True)
