from django.urls import path
from .views import QuizViewRelated,QuizDetails

urlpatterns = [
    
    
    path('quiz/',QuizViewRelated.as_view(),name="quiz"),
    path('quiz/<int:id>/', QuizDetails.as_view(),name="quiz")

]