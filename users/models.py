from .validators import validate_file_size
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser
from .manager import UserManager
from django.contrib.auth.models import Group
from django.utils import timezone


class School(models.Model):
    """Model to create School"""
    school = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    
    def __str__(self):
        return self.school

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    is_counselor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.is_counselor:
            self.is_staff = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

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


class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.user.is_counselor:
            raise ValueError("The user must be a counselor to create a Counselor object")
        super().save(*args, **kwargs)
        self.assign_default_group()

    def assign_default_group(self):
        group, created = Group.objects.get_or_create(name='Counselors')

        if group not in self.user.groups.all():
            self.user.groups.add(group)
