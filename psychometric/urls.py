from django.urls import path
from .views import PsychometricViewRelated,PsychometricDetails

urlpatterns = [
    
    
    path('psychometric/',PsychometricViewRelated.as_view(),name="PsychometricTest"),
    path('psychometric/<int:id>/', PsychometricDetails.as_view(),name="PsychometricTest")

]