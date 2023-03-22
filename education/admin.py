from django.contrib import admin
from .models import Question, Quiz, QuizResult,Answer
from nested_admin import NestedTabularInline, NestedModelAdmin
# Register your models here.

class AnswerInline(NestedTabularInline):
    model = Answer

class QuestionInline(NestedTabularInline):
    model = Question
    inlines = [
        AnswerInline,
    ]

@admin.register(Quiz)
class QuizAdmin(NestedModelAdmin):
    inlines = [QuestionInline]

admin.site.register(QuizResult)
