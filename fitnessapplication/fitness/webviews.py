from django.shortcuts import render, redirect
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .models import Exercise, Trainer, Subscription
from .forms import TrainerRegister,TrainerLogin,ExerciseForm,ExerciseItemForm
from django.contrib.auth import login, authenticate,logout
from django.forms.models import inlineformset_factory



def handler404(request,exception):
    return render(request,"404.html")
    
def home(request):

    return render(request,'home_page.html')

def registration_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = TrainerRegister()
    if request.method == "POST":
        form = TrainerRegister(request.POST)
        if form.is_valid():
            # Save the object user  
            user = form.save(commit=False)
            # hashing the password
            user.set_password(user.password)
            user.save()

            Trainer.objects.create(user=user)

            login(request,user)

            return redirect("home")
    context={
        "form":form,
    }
    return render(request,'register.html',context)

def user_login(request):
    form = TrainerLogin()
    if request.method == "POST":
        form = TrainerLogin(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                # Where you want to go after a successful login
                return redirect("home")

    context = {
        "form": form,
    }
    return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    return redirect("register-trainer")


    ## Exercise

def new_exercise(request):
    form = ExerciseForm()         
    if request.method == "POST":
        form = ExerciseForm(request.POST,request.FILES)
        if form.is_valid():
            exercise =form.save()
            exercise.trainer = request.user.trainer
            exercise.save()
                # Where you want to go after a successful login
            return redirect("home")

    context = {
        "form": form,
    }
    return render(request, "add_exercise.html", context)

def assign_exercise(request):
    form = ExerciseItemForm()    
    # formSet = setsFormset()           
    if request.method == "POST":
        form = ExerciseItemForm(request.POST,request.FILES)
        # formSet = setsFormset(request.POST)           
        if all([form.is_valid()]):
            exercise =form.save()
            # exercise.trainee = request.trainee
            exercise.save()
            # for form in formSet:
            #     child = form.save(commit=False)
            #     child.exercise = exercise
            #     child.save()
                # Where you want to go after a successful login
            return redirect("home")

    context = {
        "form": form,
        # "setsForm":formSet
    }
    return render(request, "assign_exercise.html", context)

def trainer_subcription_create_view(request):
    form = TrainerSubscriptionForm()
    if request.method == "POST":
        form = TrainerSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list-view")
    context = {
        "form": form,
    }
    return render(request, 'create_page.html', context)


def trainer_subscription_update_view(request, subscription_id):
    subscription = TrainerSubscriptionForm.objects.get(id=subscription_id)
    form = TrainerSubscriptionForm(instance=subscription)
    if request.method == "POST":
        form = TrainerSubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect("list-page")
    context = {
        "subscription": subscription,
        "form": form,
    }
    return render(request, 'object_update.html', context)


def trainer_subscription_delete_view(request, subcription_id):
    Subscription.objects.get(id=subcription_id).delete()
    return redirect("list-view")
