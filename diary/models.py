from django.db import models
from users.models import Student  # Ensure this import is correct

class WorkExperienceQuestion(models.Model):
    DAY_CHOICES = [
        ('Day1', 'Day1'),
        ('Day2', 'Day2'),
        ('Day3', 'Day3'),
        ('Day4', 'Day4'),
        ('Day5', 'Day5'),
        ('Day6', 'Day6'),
        ('Day7', 'Day7'),
        ('Day8', 'Day8'),
        ('Day9', 'Day9'),
        ('Day10', 'Day10'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    day = models.CharField(max_length=25, choices=DAY_CHOICES)
    date = models.DateField()
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"Question - {self.day} - {self.student.user.username}"
