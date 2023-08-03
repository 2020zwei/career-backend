from django.urls import path
from .views import (CvViewRelated,EducationViewRelated,JuniorCertTestViewRelated,
                    ExperienceViewRelated,ReferenceViewRelated, SkillsViewRelated,
                    QualityViewRelated,GeneratePDF,EducationViewUpdate, 
                    JuniorViewUpdate, LeavingViewUpdate,ExperienceViewUpdate,ReferenceViewUpdate,
                    SkillsUpdate,QualityUpdate, LeavingCertTestViewRelated,CVUpdate, InterestViewRelated, InterestUpdate)


urlpatterns = [
    
    
    path('create-cv/',CvViewRelated.as_view(),name="Create-Cv"),
    path('get-cv/',CvViewRelated.as_view(),name="get-Cv"),
    path('update-cv/<int:pk>/',CVUpdate.as_view(),name="Update_CV"),
    path('get-education/',EducationViewRelated.as_view(),name="Get_Education"),
    path('add-education/',EducationViewRelated.as_view(),name="Add_Education"),
    path('update-education/<int:pk>/',EducationViewUpdate.as_view(),name="Update_Education"),
    path('delete-education/<int:pk>/',EducationViewRelated.as_view(), name="Delete_Education"),
    path('add-junior-cert/',JuniorCertTestViewRelated.as_view(),name="Add_Junior_Cert"),
    path('get-junior-cert/',JuniorCertTestViewRelated.as_view(),name="Get_Junior_Cert"),
    path('update-junior/<int:pk>/',JuniorViewUpdate.as_view(),name="Update_Junior"),
    path('delete-junior-cert/<int:pk>/',JuniorCertTestViewRelated.as_view(), name="Delete_Junior"),
    path('add-leaving-cert/',LeavingCertTestViewRelated.as_view(),name="Add_Leaving_Cert"),
    path('get-leaving-cert/',LeavingCertTestViewRelated.as_view(),name="Get_Leaving_Cert"),
    path('update-leaving/<int:pk>/',LeavingViewUpdate.as_view(),name="Update_Leaving"),
    path('add-experience/',ExperienceViewRelated.as_view(),name="Add_Experience"),
    path('get-experience/',ExperienceViewRelated.as_view(),name="Get_Experience"),
    path('update-experience/<int:pk>/',ExperienceViewUpdate.as_view(),name="Update_Experience"),
    path('add-reference/',ReferenceViewRelated.as_view(),name="Add_Reference"),
    path('get-reference/',ReferenceViewRelated.as_view(),name="Get_Reference"),
    path('update-reference/<int:pk>/',ReferenceViewUpdate.as_view(),name="Update_Reference"),
    path('add-skill/',SkillsViewRelated.as_view(),name="Add_Skill"),
    path('get-skill/',SkillsViewRelated.as_view(),name="Get_Skill"),
    path('update-skill/<int:pk>/',SkillsUpdate.as_view(),name="Update_Skills"),
    path('add-interest/',InterestViewRelated.as_view(),name="Add_Interest"),
    path('get-interest/',InterestViewRelated.as_view(),name="Get_Interest"),
    path('update-interest/<int:pk>/',InterestUpdate.as_view(),name="Update_Interest"),
    
    path('cv/',GeneratePDF.as_view(),name="CV"),



    
]