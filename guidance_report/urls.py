from django.urls import path
from .views import GenerateGpt, GeneratePDFReport, GuidanceReportModels, ChatbotAPIView


urlpatterns = [
    path("get-report-models/", GuidanceReportModels.as_view(), name="report-models"),
    path('my-guidance-pdf-report/', GeneratePDFReport.as_view(), name='my-guidance-pdf-report'),
    path('generate-report/', GenerateGpt.as_view(), name='generate-report-response'),
    path('chatbot/', ChatbotAPIView.as_view(), name='chatbot'),
]
