from django.db import models
from user.models import Student

# Create your models here.

class Quiz(models.Model):
    name = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'education'

    
class Question(models.Model):
    quiz=models.ForeignKey(Quiz,related_name="question", on_delete=models.CASCADE)
    question = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question
    
    class Meta:
        app_label = 'education'

class Answer(models.Model):
    question= models.ForeignKey(Question,related_name="answer",on_delete=models.CASCADE)
    answer=models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.answer

class QuizResult(models.Model):
    user=models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    score=models.IntegerField()
    def __str__(self):
        return self.user.first_name

   
