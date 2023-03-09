from django.contrib import admin
from .models import CV,Education,JuniorCertTest,Experience,Reference,Qualities,Skills
# Register your models here.
class CVAdminSite(admin.ModelAdmin):
    list_display=['user','is_juniorcert_test']
class EducationAdminSite(admin.ModelAdmin):
    list_display=['user','year','school','examtaken']
class JuniorCertTestAdminSite(admin.ModelAdmin):
    list_display=['user','subject','level','result']
class ExperienceTestAdminSite(admin.ModelAdmin):
    list_display=['user','startdate','enddate','jobtitle','company','city','country','description']

class ReferenceAdminSite(admin.ModelAdmin):
    list_display=['cv','contactemail','position']

class SkillsAdminSite(admin.ModelAdmin):
    list_display=['user','skill','description']

class QualitiesAdminSite(admin.ModelAdmin):
    list_display=['user','quality','description']


admin.site.register(CV,CVAdminSite)
admin.site.register(Education,EducationAdminSite)
admin.site.register(JuniorCertTest,JuniorCertTestAdminSite)
admin.site.register(Experience,ExperienceTestAdminSite)
admin.site.register(Reference,ReferenceAdminSite)
admin.site.register(Skills,SkillsAdminSite)
admin.site.register(Qualities,QualitiesAdminSite)