from django.urls import path
from .views import *

urlpatterns = [
    
    
    path('choices/',ChoiceViewRelated.as_view(),name="choice"),
    path('level6/',Level6ViewRelated.as_view(),name="level6"),
    path('level8/',Level8ViewRelated.as_view(),name="level8"),
    path('level5/',Level5ViewRelated.as_view(),name="level5"),
    path('apprentice/',ApprenticeViewRelated.as_view(),name="apprentice"),
    path('other/',OtherViewRelated.as_view(),name="other"),



    
]