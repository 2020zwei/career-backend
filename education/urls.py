from django.urls import path
from .views import QuizViewRelated, QuizDetails, QuizListAPIView, TakeQuizView

urlpatterns = [
    path('quiz/',QuizViewRelated.as_view(),name="quiz"),
    path('quiz/<int:id>/', QuizDetails.as_view(),name="quiz"),
    path('quizzes/', QuizListAPIView.as_view(), name='quiz-list'),
    path('quiz-result/', TakeQuizView.as_view(), name='quiz-result')
]