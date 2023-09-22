from django.urls import path
from .views import SubjectViewRelated,SubjectGradeViewRelated,CalculatePointViewRelated, UserPointsView, UserPointsDeleteView, RemoveSubjectGradeFromUserPoints


urlpatterns = [
    path('subject-list/',SubjectViewRelated.as_view(),name="SubjectList"),
    path('check-level-grade/',SubjectGradeViewRelated.as_view(),name="CheckSubjectLevel"),
    path('calculate-coa-point/',CalculatePointViewRelated.as_view(),name="CheckSubjectLevel"),
    path('user-points/', UserPointsView.as_view(),name="UserPoints"),
    path('user-points/delete/<int:pk>/', UserPointsDeleteView.as_view(), name='userpoints-delete'),
    path('remove-subject-grade/', RemoveSubjectGradeFromUserPoints.as_view(), name='remove-subject-grade'),
]