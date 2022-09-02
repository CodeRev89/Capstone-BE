from black import re
from django.shortcuts import render, redirect
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .models import Exercise, ExerciseItem, Subscription, SubscriptionItem, Trainee, Trainer
from .forms import TrainerRegister,TrainerLogin,ExerciseForm,ExerciseItemForm, TrainerSubscriptionForm
from django.contrib.auth import login, authenticate,logout
from django.forms.models import inlineformset_factory
from django.http import JsonResponse
from django.template.loader import render_to_string



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
            user.is_trainer = True
            user.save()


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
                if auth_user.is_trainer:
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

# def trainer_exercises_list(request,trainerId):
#     trainer = Trainer.objects.get(user__id = trainerId)
#     exercises = Exercise.objects.filter(trainer=trainer).order_by("-id")
#     categories = request.GET.getlist("category[]")

#     if len(categories) > 0:
#         exercises = exercises.filter(category__id__in=categories)
   
#     filter_template = render_to_string('ajax/trainer_exercise.html', {"data": exercises})
#     return JsonResponse({"data": filter_template})

def trainer_exercises_list(request,trainerId):
    trainer = Trainer.objects.get(user__id = trainerId)
    exercises: list[Exercise] = list(Exercise.objects.filter(trainer = trainer))       

    context = {
        "exercises": exercises,
    }
    return render(request, "trainer_exercise.html", context)

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

def assign_exercise(request,traineeId):
    trainee = Trainee.objects.get(user__id=traineeId)
    setsFormset = inlineformset_factory(model= ExerciseItem, parent_model=Trainee, form=ExerciseItemForm,extra=0)
    forms = setsFormset()    
    if request.method == "POST":
        forms = setsFormset(request.POST)
        if forms.is_valid():
            for form in forms:
                child = form.save(commit=False)
                child.trainee = trainee
                child.save()
                # Where you want to go after a successful login
            return redirect("home")

    context = {
        "forms": forms,
        "trainee":trainee
    }
    return render(request, "assign_exercise.html", context)


# Subscription
def trainer_subs_list(request,trainerId):
    trainer = Trainer.objects.get(user__id = trainerId)
    subs: list[Subscription] = list(Subscription.objects.filter(trainer = trainer))       

    context = {
        "subs": subs,
    }
    return render(request, "trainer_subscriptions.html", context)

# Subscripers 
def subsripres_list(request,trainerId):
    trainer = Trainer.objects.get(user__id = trainerId)

    subsItems: list[SubscriptionItem] = list(SubscriptionItem.objects.filter(plan__trainer = trainer))       
    # subsribers: list[Trainee] = list(Trainee.objects.filter(trainer = trainer))       

    context = {
        "subsItems": subsItems,
    }
    return render(request, "subscribers.html", context)

def subcription_create_view(request):
    form = TrainerSubscriptionForm()
    if request.method == "POST":
        form = TrainerSubscriptionForm(request.POST)
        if form.is_valid():
            plan=form.save(commit=False)
            plan.trainer = request.user.trainer
            plan.save()
            return redirect(f'/subscriptions/{request.user.id}' )
    context = {
        "form": form,
    }
    return render(request, 'add_subscribtion.html', context)

def subscription_update_view(request, subscription_id):
    subscription = TrainerSubscriptionForm.objects.get(id=subscription_id)
    form = TrainerSubscriptionForm(instance=subscription)
    if request.method == "POST":
        form = TrainerSubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect(f'/subscriptions/{request.user.id}' )
    context = {
        "subscription": subscription,
        "form": form,
    }
    return render(request, 'object_update.html', context)


def subscription_delete_view(request, subId):
    sub= Subscription.objects.get(id=subId)
    if sub.trainer == request.user.trainer:
        sub.delete()
    
    return redirect(f'/subscriptions/{request.user.id}' )