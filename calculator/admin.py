from django.contrib import admin
from .models import Subject,Level,SubjectGrade,UserPoints
from users.models import Counselor

class SubjectDisplay(admin.ModelAdmin):
    list_display = ['name', 'is_additional_marks_allowed', 'additional_marks']
    search_fields = ['name', 'level__subjectlevel', 'additional_marks']
    filter_horizontal = ('level',)

class LevelAdmin(admin.ModelAdmin):
    list_display = ['subjectlevel']
    search_fields = ['subjectlevel']

class SubjectGradeAdmin(admin.ModelAdmin):
    list_display = ['subject', 'grade', 'point', 'level']
    search_fields = ['subject__name', 'grade', 'point', 'level__subjectlevel']

class UserPointsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_points']
    search_fields = ['user__full_name', 'user__school', 'grades__subject__name', 'grades__grade']
    filter_horizontal = ('grades',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(user__school=counselor.school)
        return qs

    def get_search_results(self, request, queryset, search_term):
        """Customize search to include filtering by numeric total_points."""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term.isdigit():  # If the search term is numeric, filter by total_points
            queryset |= self.model.objects.filter(total_points=search_term)

        return queryset, use_distinct

admin.site.register(Subject, SubjectDisplay)
admin.site.register(Level, LevelAdmin)
admin.site.register(SubjectGrade, SubjectGradeAdmin)
admin.site.register(UserPoints, UserPointsAdmin)