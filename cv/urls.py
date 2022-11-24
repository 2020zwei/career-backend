from django.urls import path
from .views import EducationViewRelated


urlpatterns = [
    
    
    path('add-education/',EducationViewRelated.as_view(),name="Add_Education"),
   

    
]