from django.db import models
from users.models import Student
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Goal(models.Model):
    user=models.ForeignKey(Student, on_delete=models.CASCADE)
    proffession=models.CharField(max_length=50)
    goal=models.CharField(max_length=50)
    realistic=models.BooleanField(default=False)
    countdown=models.DateTimeField(auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return self.user.full_name


# Create your models here.
class Action(models.Model):
    goal=models.ForeignKey(Goal, on_delete=models.CASCADE,related_name="action", blank=True, null=True)
    action=models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.action