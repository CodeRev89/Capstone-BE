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
from fitness import webviews as web
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from fitness.views import TrainerListView, TrainerDetailView  #TrainerSubscriptionListView

from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("trainee-register/", views.TraineeRegisterAPIView.as_view(),name="register-trainee"),
    path("trainee-login/", views.UserTokenApiView.as_view(), name="login-trainee"),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('trainer-list/', TrainerListView.as_view(), name='trainer-list'),
    path('trainer-detail/<int:object_id>/', TrainerDetailView.as_view(), name='trainer-detail'),
    #  path('trainer-subcription-list/', TrainerSubscriptionListView.as_view(), name='subs-list'),
    # path("trainer-register/", Trainer_register,name="register-trainer"),
    # path("trainer-login/", Trainer_login, name="login-trainer"),
    # path("home-page/", Trainer_homepage, name="profile-trainer"),
    
    ### WEB ###
    path("trainer-register/", web.registration_view,name="register-trainer"),
    path("trainer-login/", web.user_login,name="login-trainer"),
    path("", web.home, name="home"),
    path('logout/', web.logout_view, name="logout"),
    path('add-exercise/', web.new_exercise, name="add-exercise"),
    path("assign-exercise/", web.assign_exercise, name="assign-exercise"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)