from django.contrib import admin
from .models import Question, Quiz, QuizResult,Answer,QuizResultDetail
from nested_admin import NestedTabularInline, NestedModelAdmin
# Register your models here.

class AnswerInline(NestedTabularInline):
    model = Answer

class QuestionInline(NestedTabularInline):
    model = Question
    inlines = [
        AnswerInline,
    ]
class ResultDetailInline(NestedTabularInline):
    model = QuizResultDetail
    extra = 0


@admin.register(Quiz)
class QuizAdmin(NestedModelAdmin):
    inlines = [QuestionInline]

@admin.register(QuizResult)
class QuizResultAdmin(NestedModelAdmin):
    inlines = [ResultDetailInline]

