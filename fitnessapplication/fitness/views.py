# from django.shortcuts import render, redirect
# from rest_framework.generics import CreateAPIView
# from .serializer import TraineeRegisterSerializer, TraineeLoginSerializer
# from rest_framework.response import Response
# from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
# from rest_framework.views import APIView
# from .forms import TrainerRegister, TrainerLogin, TrainerWorkoutForm
# from django.contrib.auth import login, authenticate
# from .models import Trainer




# class TraineeRegisterAPIView(CreateAPIView):
#     serializer_class=TraineeRegisterSerializer

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
