from django.db import models
from user.models import Student
# Create your models here.

class TestType(models.Model):
    type=models.CharField(max_length=300)

    def __str__(self):
        return self.type

class PsychometricTest(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(PsychometricTest, related_name="question",on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    type=models.ForeignKey(TestType,on_delete=models.CASCADE)
    def __str__(self):
        return self.question

class Answer(models.Model):
    question= models.ForeignKey(Question,related_name="answer",on_delete=models.CASCADE)
    answer=models.CharField(max_length=300)
    weightage=models.IntegerField()
    def __str__(self):
        return self.answer

class TestResult(models.Model):
    user=models.OneToOneField(Student, on_delete=models.CASCADE)
    test=models.ForeignKey(PsychometricTest,on_delete=models.CASCADE)
    score=models.IntegerField()
    def __str__(self):
        return self.score
   
