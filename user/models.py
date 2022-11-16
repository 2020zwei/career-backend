from .validators import validate_file_size
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager



class User(AbstractUser):
    """Model to create User"""
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    school = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to='profile_images',null=True,blank=True,validators=[validate_file_size])  
    dob = models.DateField()

    username = None
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = UserManager()

    

    def __str__(self):
        """return email of User"""
        return self.email
    

