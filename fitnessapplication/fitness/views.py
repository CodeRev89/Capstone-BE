from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView,RetrieveUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import SubscriptionItem, Trainer, Subscription, ExerciseItem
from .serializer import TraineeRegisterSerializer, TraineeLoginSerializer, UserTokenSerializer,ExerciseItemSerializer, TrainerDetailSerializer, TrainerListSerializer, TrainerSubscriptionListSerializer,SubscribeSerilizer

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwner



class UserTokenApiView(TokenObtainPairView):
    serializer_class= UserTokenSerializer

class TraineeRegisterAPIView(CreateAPIView):
    serializer_class=TraineeRegisterSerializer
    
class ExerciseItemUpdateView(RetrieveUpdateAPIView):
    queryset = ExerciseItem.objects.all()
    serializer_class = ExerciseItemSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'exercise_id'
    permission_classes = [IsOwner]

class TodayExerciseListView(ListAPIView):
    queryset = ExerciseItem.objects.all()
    serializer_class = ExerciseItemSerializer
    permission_classes = [IsOwner]
    def get_queryset(self):
        return ExerciseItem.objects.filter(trainee=self.request.user.id,date=datetime.today())

class MonthlyExerciseListView(ListAPIView):
    queryset = ExerciseItem.objects.all()
    serializer_class = ExerciseItemSerializer
    permission_classes = [IsOwner]
    def get_queryset(self):
        query = self.request.GET
        month=query["month"]
        print(datetime.today().month)
        return ExerciseItem.objects.filter(trainee=self.request.user.id,date__month=month)


class TrainerListView(ListAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerListSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['specialty',"experience"]
    search_fields = ['user__username','specialty',"user__first_name","user__last_name"]




class TrainerDetailView(RetrieveAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerDetailSerializer
    lookup_field = 'user__id'
    lookup_url_kwarg = 'trainer_id'
    

# all subsc
class TrainerSubscriptionListView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = TrainerSubscriptionListSerializer

# by trainer
class TrainerSubscriptionListView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = TrainerSubscriptionListSerializer
    lookup_field = 'trainer__user__id'
    lookup_url_kwarg = 'trainer_id'

# subscribe 
class SubscribeView(CreateAPIView):
    serializer_class = SubscribeSerilizer
    permission_classes = [IsAuthenticated,]
    def perform_create(self, serializer):
        query = self.request.GET
        # date= query["end_date"]
        # end_date= datetime.strptime(date, '%Y-%m-%d').date()
        serializer.save(trainee = self.request.user.trainee )

class UpdateSubscribeView(RetrieveUpdateAPIView):
    queryset = SubscriptionItem.objects.all()
    serializer_class = SubscribeSerilizer
    lookup_field = 'id'
    lookup_url_kwarg = 'plan_id'
    permission_classes = [IsOwner,]

class MyPlansView(ListAPIView):
    serializer_class = SubscribeSerilizer
    permission_classes = [IsOwner,]
    def get_queryset(self):
        return SubscriptionItem.objects.filter(trainee=str(self.request.user.id))
    

    






    
# class TraineeLoginAPIView(APIView):
#     serializer_class = TraineeLoginSerializer

#     def post(self, request):
#         my_data = request.data
#         serializer = TraineeLoginSerializer(data=my_data)
#         if serializer.is_valid(raise_exception=True):
#             valid_data = serializer.data
#             return Response(valid_data, status=HTTP_200_OK)
#         return Response(serializer.errors, HTTP_400_BAD_REQUEST)
    
    

# def Trainer_register(request):
#     form = TrainerRegister()
#     if request.method == "POST":
#         form = TrainerRegister(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)

#             user.set_password(user.password)
#             user.save()

#             login(request, user)
#             print("you are registerd")
#             # Where you want to go after a successful signup
#             return redirect("profile-trainer")
#     context = {
#         "form": form,
#     }
#     return render(request, "register.html", context)



# def Trainer_login(request):
#     form = TrainerLogin()
#     if request.method == "POST":
#         form = TrainerLogin(request.POST)
#         if form.is_valid():

#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password"]

#             auth_user = authenticate(username=username, password=password)
#             if auth_user is not None:
#                 login(request, auth_user)
#                 print("logged in")
#                 # Where you want to go after a successful login
#                 return redirect("profile-trainer")

#     context = {
#         "form": form,
#     }
#     return render(request, "login.html", context)


# def Trainer_homepage(request):
#     # age=age.objects.all()
#     pass 


# def TrainerWorkout_create_view(request):
#     form = TrainerWorkoutForm()
#     if request.method == "POST":
#         form = TrainerWorkoutCreateForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("list-view")
#     context = {
#         "form": form,
#     }
#     return render(request, 'create_page.html', context)


# def TrainerWorkout_update_view(request, workout_id):
#     obj = TrainerWorkoutForm.objects.get(id=workout_id)
#     form = TrainerWorkoutForm(instance=workout)
#     if request.method == "POST":
#         form = TrainerWorkoutForm(request.POST, instance=workout)
#         if form.is_valid():
#             form.save()
#             return redirect("list-page")
#     context = {
#         "workout" : workout,
#         "form": form,
#     }
#     return render(request, 'workout_update.html', context)

# def TrainerWorkout_delete_view(request, workout_id):
#     TrainerWorkoutForm.objects.get(id=workout_id).delete()
#     return redirect("list-view")
