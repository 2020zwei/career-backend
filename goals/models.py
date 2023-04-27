from django.db import models
from users.models import Student
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Goal(models.Model):
    user=models.OneToOneField(Student, on_delete=models.CASCADE)
    proffession=models.CharField(max_length=50)
    goal=models.CharField(max_length=50)
    actions=models.CharField(max_length=200)
    realistic=models.BooleanField(default=False)
    countdown=models.DateTimeField(auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return self.user.full_name
