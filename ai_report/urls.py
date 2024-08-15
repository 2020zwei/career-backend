from django.urls import path
from .views import GenerateReport


urlpatterns = [
    path('generate-report/', GenerateReport.as_view(), name='generate-report'),
]