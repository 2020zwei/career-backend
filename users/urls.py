from django.urls import path
from .views import SignupUser,UserView,SchoolView  


urlpatterns = [
    
    
    path('signup/',SignupUser.as_view(),name="user-signup"),
    path('me/',UserView.as_view(),name="current-user"),
    path('schools/',SchoolView.as_view(),name="school")
]