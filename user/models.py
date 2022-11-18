from .validators import validate_file_size
from django.db import models
from django.contrib.auth.models import User





class Student(models.Model):
    """Model to create Student"""
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    school = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to='profile_images',null=True,blank=True,validators=[validate_file_size])  
    dob = models.DateField(null=True,blank=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='student')



    def __str__(self):
        
        return self.user.email





    


    

