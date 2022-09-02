from calendar import monthrange
from datetime import datetime, date,timedelta
from unicodedata import category
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters,response,status
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView,RetrieveUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import Category, Exercise, SubscriptionItem, Trainee, Trainer, Subscription, ExerciseItem
from .serializer import CategorySerilizer, ExerciseSerializer, TraineeDetailSerializer, TraineeRegisterSerializer, TraineeLoginSerializer, UserTokenSerializer,ExerciseItemSerializer, TrainerDetailSerializer, TrainerListSerializer, TrainerSubscriptionListSerializer,SubscribeSerilizer

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwner, IsProfileOwner



class UserTokenApiView(TokenObtainPairView):
    serializer_class= UserTokenSerializer

class TraineeRegisterAPIView(CreateAPIView):
    serializer_class=TraineeRegisterSerializer

class MyProfileAPIView(RetrieveUpdateAPIView):
    serializer_class=TraineeDetailSerializer
    permission_classes = [IsAuthenticated,IsProfileOwner]
    def get_object(self):
        return self.request.user.trainee

class TraineeProfileAPIView(RetrieveAPIView):
    queryset=Trainee.objects.all()
    serializer_class=TraineeDetailSerializer
    lookup_field = 'user__id'
    lookup_url_kwarg = 'trainee_id'
    
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
    

class TraineePerformance(APIView):
    def get(self,request):
        done_exercises = ExerciseItem.objects.filter(trainee = request.user.trainee, done=True,date = datetime.today())
        all_exercises = ExerciseItem.objects.filter(trainee = request.user.trainee,date = datetime.today())
        active_calories = 0
        calories = 0
        trainee = request.user.trainee
        if trainee.gender == "male":
            calories = 66 +( 6.2 * trainee.weight )+ (12.7 * trainee.height) - (6.76 * trainee.age)
        elif trainee.gender == "female":
            calories = 655.1 +( 4.35 * trainee.weight) + (4.7 * trainee.height) - (4.7 * trainee.age)
            
        for exercise in done_exercises:
            exerciseCalories = 0
            try:
                exerciseCalories = int(exercise.time.strftime("%M")) * 3 * 3.5 * request.user.trainee.weight/200
            except:
                # print(type(int(exercise.time.strftime("%M"))))
                exerciseCalories = 10 * 3 * 3.5 * 70/200
            active_calories = active_calories + exerciseCalories 
            calories = calories +active_calories
        return response.Response({"done":len(done_exercises),"all":len(all_exercises),"total_calories":calories,"active_calories":active_calories},status=status.HTTP_200_OK)

class MonthlyTraineePerformance(APIView):
    def get(self,request):
        trainee = request.user.trainee
        query = request.GET
        year = int(query["year"])
        month = int(query["month"])
        # plan = SubscriptionItem.objects.get(trainee=trainee)
        # start_date = plan.start_date
        # end_date = plan.end_date
        # days = pandas.date_range(start_date,end_date,freq='d')
        num_days = monthrange(year, month)
        days = [date(year, month, day) for day in range(1, num_days[1]+1)]
        final=[]
        for day in days:
            done_exercises = ExerciseItem.objects.filter(trainee = trainee, done=True,date = day)
            all_exercises = ExerciseItem.objects.filter(trainee = trainee,date =day)
            active_calories = 0
            calories = 0
            if trainee.gender == "male":
                calories = 66 +( 6.2 * trainee.weight )+ (12.7 * trainee.height) - (6.76 * trainee.age)
            elif trainee.gender == "female":
                calories = 655.1 +( 4.35 * trainee.weight) + (4.7 * trainee.height) - (4.7 * trainee.age)
            for exercise in done_exercises:
                exerciseCalories = 0
                try:
                    exerciseCalories = int(exercise.time.strftime("%M")) * 3 * 3.5 * trainee.weight/200
                except:
                    exerciseCalories = 10 * 3 * 3.5 * 70/200
                active_calories = active_calories + exerciseCalories 
                calories = calories +active_calories
            data = {"date":day,"done":len(done_exercises),"all":len(all_exercises),"total_calories":calories,"active_calories":active_calories}
            final.append(data)
        return response.Response(final,status=status.HTTP_200_OK)

class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerilizer

class SampleExerciseView(ListAPIView):
    serializer_class=ExerciseSerializer
    def get_queryset(self):
        exercises = []
        trainers = Trainer.objects.all()
        category=Category.objects.get(id=self.request.GET["category_id"])

        for trainer in trainers:
            trainer_exercises = Exercise.objects.filter(trainer=trainer, category=category)
            if len(trainer_exercises)>0:
                exercises.append(trainer_exercises.first())
        
        return exercises
        