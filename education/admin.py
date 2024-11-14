from django.contrib import admin
from .models import Question, Quiz, QuizResult, Answer, QuizResultDetail, QuizLimit
from nested_admin import NestedTabularInline, NestedModelAdmin
from users.models import Counselor


# Inline for Answers
class AnswerInline(NestedTabularInline):
    model = Answer
    extra = 1


# Inline for Questions
class QuestionInline(NestedTabularInline):
    model = Question
    inlines = [AnswerInline]
    extra = 1


# Inline for Quiz Result Details
class ResultDetailInline(NestedTabularInline):
    model = QuizResultDetail
    extra = 0


# Quiz Admin
@admin.register(Quiz)
class QuizAdmin(NestedModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description', 'youtube_title', 'youtube_link']
    inlines = [QuestionInline]


# Quiz Result Admin
@admin.register(QuizResult)
class QuizResultAdmin(NestedModelAdmin):
    list_display = ['user', 'quiz', 'score']
    search_fields = ['user__full_name', 'quiz__name', 'score']
    inlines = [ResultDetailInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(user__school=counselor.school)
        return qs


# Quiz Limit Admin
@admin.register(QuizLimit)
class QuizLimitAdmin(admin.ModelAdmin):
    list_display = ['limit']
    search_fields = ['limit']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs.count() > 1:
            qs = qs[:1]
        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            if QuizLimit.objects.exists():
                raise ValueError("Only one QuizLimit instance is allowed.")
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        if QuizLimit.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if obj is None and QuizLimit.objects.exists():
            return False
        return super().has_change_permission(request, obj)


# Admin for Questions
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question']
    search_fields = ['quiz__name', 'question']


# Admin for Answers
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'is_correct']
    search_fields = ['question__question', 'answer', 'is_correct']


# Admin for Quiz Result Details
@admin.register(QuizResultDetail)
class QuizResultDetailAdmin(admin.ModelAdmin):
    list_display = ['result', 'question', 'answer']
    search_fields = ['result__user__full_name', 'question__question', 'answer__answer']
