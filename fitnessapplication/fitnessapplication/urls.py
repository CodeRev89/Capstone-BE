"""fitnessapplication URL Configuration

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
from django.urls import path
from fitness import views
from fitness.views import Trainer_register, Trainer_login, Trainer_homepage
# from .settings import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("trainee-register/", views.TraineeRegisterAPIView.as_view(),name="register-trainee"),
    path("trainee-login/", views.TraineeLoginAPIView.as_view(), name="login-trainee"),
    path("trainer-register/", Trainer_register,name="register-trainer"),
    path("trainer-login/", Trainer_login, name="login-trainer"),
    path("home-page/", Trainer_homepage, name="profile-trainer"),
    
    
]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)