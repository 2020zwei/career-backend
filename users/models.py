from .validators import validate_file_size
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

class School(models.Model):
    """Model to create School"""
    school = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    
    def __str__(self):
        return self.school

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

class Student(models.Model):
    """Model to create Student"""
    
    first_name = models.CharField(max_length=100,blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=100)
    school =  models.CharField(max_length=50, blank=True,null=True)
    profile_image = models.ImageField(upload_to='profile_images',null=True,blank=True,validators=[validate_file_size],max_length=255)

    dob = models.DateField(null=True,blank=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='student')
    city = models.CharField(max_length=50, blank=True,null=True)
    country = models.CharField(max_length=50, blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    address2 = models.TextField(blank=True,null=True)
    number = models.DecimalField(decimal_places=0, max_digits=15, blank=True,null=True)
    eircode=models.CharField(max_length=7,null=True,blank=True)
    otp = models.CharField(max_length=5,null=True, blank=True)
    cv_completed=models.BooleanField(default=False)
    otp_verified = models.BooleanField(default=False)
    current_step = models.IntegerField(default=1)

    def __str__(self):
        """return name of Student"""
        return self.full_name
 

