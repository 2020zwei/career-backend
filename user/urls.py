from django.urls import path
from .views import UserLoginView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    
    path('login/',UserLoginView.as_view(),name="user-login"),
    
]