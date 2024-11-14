from django.contrib import admin
from .models import CV, Education, JuniorCertTest, Experience, Reference, Qualities, Skills, JobTitle, LeavingCertTest, Interests, AdditionalInfo
from users.models import Counselor

class CVAdminSite(admin.ModelAdmin):
    list_display = ['user', 'is_juniorcert_test']
    search_fields = ['user__full_name', 'skills', 'HobbiesandInterests', 'objective', 'city', 'town', 'email']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(user__school=counselor.school)
        return qs


class EducationAdminSite(admin.ModelAdmin):
    list_display = ['user', 'year', 'school', 'examtaken']
    search_fields = ['user__full_name', 'school', 'examtaken', 'year']


class JuniorCertTestAdminSite(admin.ModelAdmin):
    list_display = ['user', 'subject', 'level', 'result']
    search_fields = ['user__full_name', 'subject', 'level', 'result']


class LeavingCertTestAdminSite(admin.ModelAdmin):
    list_display = ['user', 'subject', 'level', 'result']
    search_fields = ['user__full_name', 'subject', 'level', 'result']


class ExperienceTestAdminSite(admin.ModelAdmin):
    list_display = ['user', 'startdate', 'enddate', 'job_title', 'company', 'city', 'country', 'description']
    search_fields = ['user__full_name', 'job_title', 'company', 'city', 'country', 'description']


class ReferenceAdminSite(admin.ModelAdmin):
    list_display = ['user_title', 'name', 'job_title', 'contact_number', 'organization_address', 'area_code', 'email']
    search_fields = ['user__full_name', 'name', 'job_title__title', 'contact_number', 'email', 'organization_address']


class SkillsAdminSite(admin.ModelAdmin):
    list_display = ['user', 'skill', 'skill_dropdown', 'description']
    search_fields = ['user__full_name', 'skill', 'skill_dropdown', 'description']


class QualitiesAdminSite(admin.ModelAdmin):
    list_display = ['user', 'quality', 'interest', 'description']
    search_fields = ['user__full_name', 'quality', 'interest', 'description']


class JobTitleAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


class InterestAdmin(admin.ModelAdmin):
    list_display = ['user', 'interests', 'description']
    search_fields = ['user__full_name', 'interests', 'description']


class AdditionalInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'additional_info']
    search_fields = ['user__full_name', 'additional_info']


# Registering Models with Updated Admin Configuration
admin.site.register(CV, CVAdminSite)
admin.site.register(Education, EducationAdminSite)
admin.site.register(JuniorCertTest, JuniorCertTestAdminSite)
admin.site.register(LeavingCertTest, LeavingCertTestAdminSite)
admin.site.register(Experience, ExperienceTestAdminSite)
admin.site.register(Reference, ReferenceAdminSite)
admin.site.register(Skills, SkillsAdminSite)
admin.site.register(Qualities, QualitiesAdminSite)
admin.site.register(JobTitle, JobTitleAdmin)
admin.site.register(Interests, InterestAdmin)
admin.site.register(AdditionalInfo, AdditionalInfoAdmin)
