from django.urls import path
from .views import GoalViewRelated,GoalDetail,GoalViewRelated2, GoalPDF

urlpatterns = [   
    path('goal/',GoalViewRelated.as_view(),name="goal"),
    path('',GoalViewRelated2.as_view(),name="goal2"),
    path('goalPdf/',GoalPDF.as_view(),name="goalPDF"),
    path('goal/<int:pk>/',GoalDetail.as_view(),name="goal"),
]