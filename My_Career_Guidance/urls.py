"""My_Career_Guidance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from users.views import CustomTokenObtainPairView
from users.serializers import CustomTokenCreateSerializer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/jwt/create', CustomTokenObtainPairView.as_view(), name='token_create'),
    path('user/',include("users.urls")),
    path('timetable/',include("timetable.urls")),
    path('calculator/',include("calculator.urls")),
    path('cv/',include("cv.urls")),
    path('psychometric/',include("psychometric.urls")),
    path('_nested_admin/', include('nested_admin.urls')),
    path('goals/', include("goals.urls")),
    path('education/', include("education.urls")),
    path('choices/', include("choices.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "My Career Guidance"
admin.site.site_title = "Career Guidance Admin Portal"
admin.site.index_title = "Welcome to Career Guidance Portal"