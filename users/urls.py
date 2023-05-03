from django.urls import path
from .views import SignupUser,UserView,SchoolView, SendPasswordResetOTPView, OTPConfirmationAPIView, ResetPasswordAPIView, UserUpdate


urlpatterns = [
    
    
    path('signup/',SignupUser.as_view(),name="user-signup"),
    path('me/',UserView.as_view(),name="current-user"),
    path('me/<int:pk>/',UserUpdate.as_view(),name="update-user"),
    path('schools/',SchoolView.as_view(),name="school"),
    path("forget-password/otp",SendPasswordResetOTPView.as_view()),
    path("otp/confirm",OTPConfirmationAPIView.as_view()),
    path("reset-password",ResetPasswordAPIView.as_view()),
]