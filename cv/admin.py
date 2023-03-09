from django.contrib import admin
from .models import CV,Education,JuniorCertTest,Experience,Reference,JobTitle
# Register your models here.
class CVAdminSite(admin.ModelAdmin):
    list_display=['user','is_juniorcert_test']
class EducationAdminSite(admin.ModelAdmin):
    list_display=['user','year','school','examtaken']
class JuniorCertTestAdminSite(admin.ModelAdmin):
    list_display=['user','subject','level','result']
class ExperienceTestAdminSite(admin.ModelAdmin):
    list_display=['user','startdate','enddate','position','company']

class ReferenceAdminSite(admin.ModelAdmin):
    list_display=['cv','user_title','name','job_title','contact_number','organization_address','area_code','email']

class JobTitleAdmin(admin.ModelAdmin):
    list_display=['title']

admin.site.register(CV,CVAdminSite)
admin.site.register(Education,EducationAdminSite)
admin.site.register(JuniorCertTest,JuniorCertTestAdminSite)
admin.site.register(Experience,ExperienceTestAdminSite)
admin.site.register(Reference,ReferenceAdminSite)
admin.site.register(JobTitle,JobTitleAdmin)