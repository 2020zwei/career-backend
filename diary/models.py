from django.db import models
from users.models import Student  # Ensure this import is correct

class WorkExperienceQuestion(models.Model):
    DAY_CHOICES = [
        ('Day 1', 'Day 1'),
        ('Day 2', 'Day 2'),
        ('Day 3', 'Day 3'),
        ('Day 4', 'Day 4'),
        ('Day 5', 'Day 5'),
        ('Day 6', 'Day 6'),
        ('Day 7', 'Day 7'),
        ('Day 8', 'Day 8'),
        ('Day 9', 'Day 9'),
        ('Day 10', 'Day 10'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    day = models.CharField(max_length=25, choices=DAY_CHOICES)
    date = models.DateField()
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"Question - {self.day} - {self.student.user.username}"
