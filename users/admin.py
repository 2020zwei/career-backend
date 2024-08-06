from django.contrib import admin
from .models import Student, School, User, Counselor


class StudentAdminDisplay(admin.ModelAdmin):
    list_display = ['__str__', 'firstname_and_lastname', 'school', 'dob', 'profile_image', 'cv_completed']

    def firstname_and_lastname(self, obj):
        return "%s %s" % (obj.first_name, obj.last_name)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(school=counselor.school)
        return qs


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username']
    search_fields = ['email', 'id']


class CounselorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'school']
    search_fields = ['user__email', 'school__school']
    list_filter = ['school']


admin.site.register(Counselor, CounselorAdmin)
admin.site.register(Student,StudentAdminDisplay)
admin.site.register(School)
admin.site.register(User, UserAdmin)

