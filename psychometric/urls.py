from django.urls import path
from .views import PsychometricViewRelated

urlpatterns = [
    
    
    path('psychometric/',PsychometricViewRelated.as_view(),name="PsychometricTest"),
    path('psychometric/<int:pk>/', PsychometricViewRelated.as_view(),name="PsychometricTest")

]