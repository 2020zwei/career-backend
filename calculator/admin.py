from django.contrib import admin
from .models import Subject,Level,SubjectGrade,UserPoints
class SubjectDisplay(admin.ModelAdmin):

    filter_horizontal = ('level',)


class SubjectGradeAdmin(admin.ModelAdmin):
    list_display = ['subject', 'grade', 'point', 'level']



admin.site.register(Subject,SubjectDisplay)
admin.site.register(Level)
admin.site.register(SubjectGrade, SubjectGradeAdmin)
admin.site.register(UserPoints)
