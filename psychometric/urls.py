from django.urls import path
from .views import PsychometricViewRelated,PsychometricDetails,CalculatePoints, PsychometricTestView, TakeTestView, TestTypeView,TestResultDetailAPIView

urlpatterns = [   
    path('psychometric/',PsychometricViewRelated.as_view(),name="PsychometricTest"),
    path('psychometric/<int:id>/', PsychometricDetails.as_view(),name="PsychometricTest"),
    path('calculate/', CalculatePoints.as_view(),name="CalculatePoint"),
    path('test/', PsychometricTestView.as_view(),name="all-psycometric"),
    path('take-test/', TakeTestView.as_view(), name='take-test'),
    path('testType/', TestTypeView.as_view(), name='test-type'),
    path('result/<int:id>/', TestResultDetailAPIView.as_view(),name="Test Result"),
    path('result', TestResultDetailAPIView.as_view(),name="View Test Result"),
]