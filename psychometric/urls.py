from django.urls import path
from .views import PsychometricViewRelated,PsychometricDetails,CalculatePoints

urlpatterns = [
    
    
    path('psychometric/',PsychometricViewRelated.as_view(),name="PsychometricTest"),
    path('psychometric/<int:id>/', PsychometricDetails.as_view(),name="PsychometricTest"),
    path('calculate/<int:id>/', CalculatePoints.as_view(),name="CalculatePoint")

]