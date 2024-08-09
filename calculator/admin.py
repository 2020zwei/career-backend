from django.contrib import admin
from .models import Subject,Level,SubjectGrade,UserPoints
from users.models import Counselor
class SubjectDisplay(admin.ModelAdmin):

    filter_horizontal = ('level',)


class SubjectGradeAdmin(admin.ModelAdmin):
    list_display = ['subject', 'grade', 'point', 'level']

class UserPointsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_points']
    search_fields = ("user__full_name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(user__school=counselor.school)
        return qs

admin.site.register(Subject,SubjectDisplay)
admin.site.register(Level)
admin.site.register(SubjectGrade, SubjectGradeAdmin)
admin.site.register(UserPoints, UserPointsAdmin)
