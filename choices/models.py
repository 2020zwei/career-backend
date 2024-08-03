from django.db import models
from users.models import Student

# Create your models here.

class Choice(models.Model):
    user=models.ForeignKey(Student, on_delete=models.CASCADE)
    level6= models.BooleanField(default=False)
    Level5= models.BooleanField(default=False)
    level8= models.BooleanField(default=False)
    other=models.BooleanField(default=False)
    apprentice= models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.full_name
    
    class Meta:
        app_label = 'choices'

    
class Level6(models.Model):
    choice=models.ForeignKey(Choice,related_name="lvl6", on_delete=models.CASCADE)
    code = models.CharField(max_length=50, null=True, blank=True, unique=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    point=models.CharField(max_length=50,null=True,blank=True)
    college=models.CharField(max_length=300,null=True,blank=True)
    url=models.CharField(max_length=300, null=True,blank=True)
    order_number = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.choice.user.full_name
    
    class Meta:
        app_label = 'choices'


class Level8(models.Model):
    choice=models.ForeignKey(Choice,related_name="lvl8", on_delete=models.CASCADE)
    code = models.CharField(max_length=50, null=True, blank=True, unique=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    point=models.CharField(max_length=50,null=True,blank=True)
    college=models.CharField(max_length=300,null=True,blank=True)
    url=models.CharField(max_length=300, null=True,blank=True)
    order_number = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.choice.user.full_name
    
    class Meta:
        app_label = 'choices'


class Apprentice(models.Model):
    choice = models.ForeignKey(Choice, related_name="app", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    level = models.CharField(max_length=50, null=True, blank=True)
    company = models.CharField(max_length=50, null=True, blank=True)
    url=models.CharField(max_length=50, null=True,blank=True)
    order_number = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.choice.user.full_name
    
    class Meta:
        app_label = 'choices'


class Level5(models.Model):
    choice=models.ForeignKey(Choice,related_name="lvl5", on_delete=models.CASCADE)
    code = models.CharField(max_length=50, null=True, blank=True, unique=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    college=models.CharField(max_length=300,null=True,blank=True)
    url=models.CharField(max_length=300, null=True,blank=True)
    order_number = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.choice.user.full_name
    
    class Meta:
        app_label = 'choices'


class Other(models.Model):
    choice=models.ForeignKey(Choice,related_name="othr", on_delete=models.CASCADE)
    idea=models.CharField(max_length=50,null=True,blank=True)
    order_number = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.choice.user.full_name
    
    class Meta:
        app_label = 'choices'


# admin models for data from spreadsheet
class AdminLevel5(models.Model):
    code = models.CharField(max_length=50, null=True, blank=True, unique=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    college = models.CharField(max_length=300, null=True, blank=True)
    url = models.CharField(max_length=300, null=True, blank=True)
    order_number = models.PositiveIntegerField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.title}"


class AdminLevel6(models.Model):
    code = models.CharField(max_length=50, null=True, blank=True, unique=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    point = models.CharField(max_length=50, null=True, blank=True)
    college = models.CharField(max_length=300, null=True, blank=True)
    url = models.CharField(max_length=300, null=True, blank=True)
    order_number = models.PositiveIntegerField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.title}"


class AdminLevel8(models.Model):
    code = models.CharField(max_length=50, null=True, blank=True, unique=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    point = models.CharField(max_length=50, null=True, blank=True)
    college = models.CharField(max_length=300, null=True, blank=True)
    url = models.CharField(max_length=300, null=True, blank=True)
    order_number = models.PositiveIntegerField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.code} - {self.title}"

