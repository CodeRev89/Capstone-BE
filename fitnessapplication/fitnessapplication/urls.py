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

from django.conf import settings





urlpatterns = [
    path("admin/", admin.site.urls),
    # AUTH
    path("trainee-register/", views.TraineeRegisterAPIView.as_view(),name="register-trainee"),
    path("trainee-login/", views.UserTokenApiView.as_view(), name="login-trainee"),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    #Profile
    path("my-profile/", views.MyProfileAPIView.as_view(), name="my-profile"), # Edit and View My profile
    path("trainee/<int:trainee_id>", views.TraineeProfileAPIView.as_view(), name="trainee"),

    #Trainers
    path('trainer-list/', views.TrainerListView.as_view(), name='trainer-list'),
    path('trainer-detail/<int:trainer_id>/', views.TrainerDetailView.as_view(), name='trainer-detail'),

    #Trainers Subscriptions
    path('trainer-subcription-list/<int:trainer_id>/', views.TrainerSubscriptionListView.as_view(), name='trainer-subs-list'),
    path('subcriptions/', views.SubscriptionListView.as_view(), name='subs-list'),

    #Exercises Items
    path('exercise/<int:exercise_id>', views.ExerciseItemUpdateView.as_view(), name =' trainee-exersize'),
    path('my-exercises/today', views.TodayExerciseListView.as_view(), name =' my-exersises'),
    path('my-exercises/monthly', views.MonthlyExerciseListView.as_view(), name =' my-exersises-monthly'),

    #Subscribtions
    path('my-plans/', views.MyPlansView.as_view(), name =' my-plans'),
    path('subscribe', views.SubscribeView.as_view(), name =' subscribe'),
    path('update/plan/<int:plan_id>', views.ReSubscribeView.as_view(), name =' renew'),

    #user Performance
    path('performace', views.TraineePerformance.as_view(), name ='performance'),
    path('performace/monthly', views.MonthlyTraineePerformance.as_view(), name ='monthly-performance'),

    #categories
    path('categories/',views.CategoryView.as_view(), name ='categories'),
    path('samples/',views.SampleExerciseView.as_view(), name ='samples'),

    
    ### WEB ###
    path("trainer-register/", web.registration_view,name="register-trainer"),
    path("trainer-login/", web.user_login,name="login-trainer"),
    path("", web.home, name="home"),
    path('logout/', web.logout_view, name="logout"),
    path('add-exercise/', web.new_exercise, name="add-exercise"),
    path("assign-exercise/<int:traineeId>", web.assign_exercise, name="assign-exercise"),
    path("exercises/<int:trainerId>", web.trainer_exercises_list, name="exercises"),
    path("subscriptions/<int:trainerId>", web.trainer_subs_list, name="subscriptions"),
    path("subscribers/<int:trainerId>", web.subsripres_list, name="subscribers"),
    path("add-subscription/", web.subcription_create_view, name="add-subscription"),
    path("delete-subscription/<int:subId>", web.subscription_delete_view, name="delete-subscription"),
    # error view
    path("404/", web.error_view, name="error"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)