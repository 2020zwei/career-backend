from django.urls import path
from .views import CvViewRelated,EducationViewRelated,JuniorCertTestViewRelated,ExperienceViewRelated,ReferenceViewRelated, SkillsViewRelated,QualityViewRelated,GeneratePDF


urlpatterns = [
    
    
    path('create-cv/',CvViewRelated.as_view(),name="Create-Cv"),
    path('add-education/',EducationViewRelated.as_view(),name="Add_Education"),
    path('add-junior-cert/',JuniorCertTestViewRelated.as_view(),name="Add_Junior_Cert"),
    path('add-leaving-cert/',JuniorCertTestViewRelated.as_view(),name="Add_Leaving_Cert"),
    path('add-experience/',ExperienceViewRelated.as_view(),name="Add_Experience"),
    path('add-reference/',ReferenceViewRelated.as_view(),name="Add_Reference"),
    path('add-skill/',SkillsViewRelated.as_view(),name="Add_Skill"),
    path('add-quality/',QualityViewRelated.as_view(),name="Add_Quality"),
    path('cv/',GeneratePDF.as_view(),name="CV"),



    
]