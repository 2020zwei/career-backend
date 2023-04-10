from django.db import models
from users.models import Student
from .choices import DAY_OF_THE_WEEK







class Slot(models.Model):
    """Model to create TimeTable"""
    
    timeslot = models.TimeField(auto_now=False, auto_now_add=False,null=True)
    endslot= models.TimeField(auto_now=False, auto_now_add=False,null=True)
    day = models.CharField(choices=DAY_OF_THE_WEEK.choices,max_length=1)
    year = models.PositiveSmallIntegerField()
    week = models.PositiveSmallIntegerField()
    user=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='Student')

    def __str__(self):
        
        return (self.user.first_name +" " + self.user.last_name)

    


    

