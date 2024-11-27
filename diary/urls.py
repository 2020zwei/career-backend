from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import WorkExperienceQuestionViewSet

router = DefaultRouter()
router.register(r'api/work-experience-questions', WorkExperienceQuestionViewSet, basename='work-experience-question')

urlpatterns = [
    path('', include(router.urls)),
    path('api/work-experience-questions/update-day/', WorkExperienceQuestionViewSet.as_view({'put': 'update_day'}), name='update-day'),
]
