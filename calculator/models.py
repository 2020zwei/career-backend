from django.db import models
from .choices import SUBJECT_LEVELS


class Level(models.Model):
    subjectlevel=models.CharField(choices=SUBJECT_LEVELS.choices,max_length=10)
    verbose_name_plural = "Levels"
    def __str__(self):
        
        return self.subjectlevel


class Subject(models.Model):
    """Model to create Subject"""
    name = models.TextField(unique=True)
    level = models.ManyToManyField(Level, related_name='subject_level',blank=True)
    is_additional_marks_allowed=models.BooleanField(default=False)
    additional_marks=models.PositiveSmallIntegerField(blank=True,null=True)
    def __str__(self):
        """return name of subject"""
        return self.name
    
    class Meta:
        verbose_name_plural = "Subjects"

class SubjectGrade(models.Model):
    """Model to create Subject"""
    grade = models.CharField(max_length=5,unique=True)
    point=models.IntegerField()
    level = models.ForeignKey(Level,on_delete=models.CASCADE, related_name='subject_grade',blank=True)

    def __str__(self):
        """return name of subject"""
        return (self.grade + " " + str(self.point) )
    
    class Meta:
        verbose_name_plural = "Grades"





