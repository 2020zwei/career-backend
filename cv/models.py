from django.db import models
from users.models import Student
from .choices import JUNIOR_CERT_TEST_LEVEL,JUNIOR_CERT_TEST_RESULT, JOB_TITLE,USER_TITLE,SUBJECTS,LEAVING_CERT_TEST_LEVEL,LEAVING_CERT_TEST_RESULT, SKILLS, QUALITY, SKILLS_DESCRIPTIONS, QUALITY_DESCRIPTIONS
from django.contrib.postgres.fields import ArrayField

class CV(models.Model):
    user=models.ForeignKey(Student, on_delete=models.CASCADE)
    objective=models.TextField(max_length=300,null=True, blank=True)
    is_juniorcert_test=models.BooleanField(default=False)
    skills=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    number = models.DecimalField(decimal_places=0, max_digits=15, blank=True,null=True)
    HobbiesandInterests=models.TextField(max_length=300,null=True)
    full_name = models.CharField(max_length     =100, null=True)
    school =  models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=50, blank=True,null=True)
    town = models.CharField(max_length=50, blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    address2 = models.TextField(blank=True,null=True)
    eircode=models.CharField(max_length=10,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)


    def __str__(self):
        return self.user.full_name
       

class Education(models.Model):
    year=models.DateField(null=True, blank=True)
    school = models.CharField(max_length=50,null=True, blank=True)
    examtaken=models.CharField(max_length=50,null=True, blank=True)
    enddate=models.DateField(null=True, blank=True)
    present=models.BooleanField(default=False)
    user=models.ForeignKey(Student, on_delete=models.CASCADE)

class JuniorCertTest(models.Model):
    subject = models.CharField(max_length=50, null=True)
    level=models.CharField(choices=JUNIOR_CERT_TEST_LEVEL.choices,max_length=2,null=True, blank=True)
    result=models.CharField(choices=JUNIOR_CERT_TEST_RESULT.choices,max_length=2,null=True, blank=True)
    user=models.ForeignKey(Student, on_delete=models.CASCADE)

class LeavingCertTest(models.Model):
    subject = models.CharField(max_length=50, null=True)
    level=models.CharField(choices=LEAVING_CERT_TEST_LEVEL.choices,max_length=2)
    result=models.CharField(choices=LEAVING_CERT_TEST_RESULT.choices,max_length=2)
    user=models.ForeignKey(Student, on_delete=models.CASCADE)

class Experience(models.Model):
    startdate = models.DateField(null=True, blank=True)
    enddate=models.DateField(null=True, blank=True)
    jobtitle=models.CharField(choices=JOB_TITLE.choices,max_length=1)
    job_title=models.CharField(max_length=50, null=True)
    company=models.CharField(max_length=50, null=True)
    city=models.CharField(max_length=50, null=True)
    country=models.CharField(max_length=50, null=True)
    description=models.TextField(max_length=300, null=True)
    is_current_work=models.BooleanField(default=False)
    user=models.ForeignKey(Student, on_delete=models.CASCADE)


class Skills(models.Model):
    skill=models.CharField(max_length=50, null=True)
    skill_dropdown=models.CharField(choices=SKILLS.choices,max_length=2,null=True, blank=True)
    description=models.TextField(max_length=300, blank=True)
    user=models.ForeignKey(Student,on_delete=models.CASCADE)

    @property
    def skill_dropdown_description(self):
        return SKILLS_DESCRIPTIONS.get(self.skill_dropdown, "")
    
    def save(self, *args, **kwargs):
        self.description = self.skill_dropdown_description
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural="skills"

class Qualities(models.Model):
    quality=models.CharField(max_length=50, null=True)
    interest=models.TextField(max_length=300,null=True, blank=True)
    quality_dropdown=models.CharField(choices=QUALITY.choices,max_length=2,null=True, blank=True)
    description=models.TextField(max_length=300, blank=True)
    user=models.ForeignKey(Student,on_delete=models.CASCADE)

    @property
    def quality_dropdown_description(self):
        return QUALITY_DESCRIPTIONS.get(self.quality_dropdown, "")
    
    def save(self, *args, **kwargs):
        self.description = self.quality_dropdown_description
        super().save(*args, **kwargs)

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
    position=models.CharField(max_length=50,null=True,blank=True)
    user=models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)

class Interests(models.Model):
    interests=models.CharField(max_length=50, null=True)
    description=models.TextField(max_length=300)
    user=models.ForeignKey(Student,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="Interests"


class AdditionalInfo(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    additional_info = models.TextField(max_length=300, default="""Any further information which might support an application such as
          membership of an organisation or the ability to speak another
          language.""")

    class Meta:
        verbose_name_plural="additional_info"
