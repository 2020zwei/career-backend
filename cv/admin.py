from django.contrib import admin
from .models import CV,Education,JuniorCertTest,Experience,Reference,Qualities,Skills,JobTitle,LeavingCertTest, Interests
# Register your models here.
class CVAdminSite(admin.ModelAdmin):
    list_display=['user','is_juniorcert_test']
class EducationAdminSite(admin.ModelAdmin):
    list_display=['user','year','school','examtaken']
class JuniorCertTestAdminSite(admin.ModelAdmin):
    list_display=['user','subject','level','result']
class LeavingCertTestAdminSite(admin.ModelAdmin):
    list_display=['user','subject','level','result']
class ExperienceTestAdminSite(admin.ModelAdmin):
    list_display=['user','startdate','enddate','job_title','company','city','country','description']

class ReferenceAdminSite(admin.ModelAdmin):
    list_display=['user_title','name','job_title','contact_number','organization_address','area_code','email']

class SkillsAdminSite(admin.ModelAdmin):
    list_display=['user','skill','skill_dropdown','description']

class QualitiesAdminSite(admin.ModelAdmin):
    list_display=['user','quality','interest','description']

class JobTitleAdmin(admin.ModelAdmin):
    list_display=['title']

class InterestAdmin(admin.ModelAdmin):
    list_display=['user','interests']

admin.site.register(CV,CVAdminSite)
admin.site.register(Education,EducationAdminSite)
admin.site.register(JuniorCertTest,JuniorCertTestAdminSite)
admin.site.register(LeavingCertTest,LeavingCertTestAdminSite)
admin.site.register(Experience,ExperienceTestAdminSite)
admin.site.register(Reference,ReferenceAdminSite)
admin.site.register(Skills,SkillsAdminSite)
admin.site.register(Qualities,QualitiesAdminSite)
admin.site.register(JobTitle,JobTitleAdmin)
admin.site.register(Interests,InterestAdmin)
