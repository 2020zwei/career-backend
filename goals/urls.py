from django.urls import path
from .views import GoalViewRelated,GoalDetail

urlpatterns = [   
    path('goal/',GoalViewRelated.as_view(),name="goal"),
    path('goal/<int:pk>/',GoalDetail.as_view(),name="goal"),
]