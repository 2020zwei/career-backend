from django.urls import path
from .views import GoalViewRelated,GoalDetail,GoalViewRelated2

urlpatterns = [   
    path('goal/',GoalViewRelated.as_view(),name="goal"),
    path('',GoalViewRelated2.as_view(),name="goal2"),
    path('goal/<int:pk>/',GoalDetail.as_view(),name="goal"),
]