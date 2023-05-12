from django.urls import path
from .views import *

urlpatterns = [
    
    
    path('choices/',ChoiceViewRelated.as_view(),name="choice"),
    path('column-names/', ColumnNamesView.as_view()),
    path('selected/',SelectedChoice.as_view(),name="selected_choice"),
    path('level6/',Level6ViewRelated.as_view(),name="level6"),
    path('update-level6/<int:pk>/',Level6Update.as_view(),name="Update_level6"),
    path('level8/',Level8ViewRelated.as_view(),name="level8"),
    path('update-level8/<int:pk>/',Level8Update.as_view(),name="Update_level8"),
    path('level5/',Level5ViewRelated.as_view(),name="level5"),
    path('update-level5/<int:pk>/',Level5Update.as_view(),name="Update_level5"),
    path('apprentice/',ApprenticeViewRelated.as_view(),name="apprentice"),
    path('update-app/<int:pk>/',ApprenticeUpdate.as_view(),name="Update_Apprentice"),
    path('other/',OtherViewRelated.as_view(),name="other"),



    
]