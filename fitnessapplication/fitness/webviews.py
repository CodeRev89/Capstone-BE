from django.shortcuts import render, redirect
from .models import Exercise, ExerciseItem, Subscription, SubscriptionItem, Trainee, Trainer
from .forms import EditTrainerProfileForm, TrainerRegister,TrainerLogin,ExerciseForm,ExerciseItemForm, TrainerSubscriptionForm
from django.contrib.auth import login, authenticate,logout
from django.forms.models import inlineformset_factory



def handler404(request,exception):
    return render(request,"pages/404.html")


# when the user logs in as a "Trainee" instead of a "Trainer"
def handler403(request):
    return render(request, 'pages/403.html')


def home(request):
    return render(request,'pages/home_page.html')


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
    return render(request,'modals/register.html',context)



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
                else: 
                    return redirect("forbidden")
    context = {
        "login": form,
    }
    return render(request, "modals/login.html", context)



def logout_view(request):
    logout(request)
    return redirect("home")



# profile view
def profile_view(request):
    trainer = Trainer.objects.get(user_id=request.user.id)
    context = {
        "profile": trainer
    }
    return render(request, "pages/profile_page.html", context)



# edit Trainer Profile!
def trainer_edit_profile(request):
    trainer = Trainer.objects.get(user_id=request.user.id)
    form = EditTrainerProfileForm(instance=trainer)
    if request.method == "POST":
        form = EditTrainerProfileForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            trainer_user = form.save()
            trainer_user.user = trainer.user
            trainer_user.save()
            return redirect("trainer-profile")
    context = {
        "form": form,
    }
    return render(request, 'pages/edit_profile.html', context)



# list of workouts by the trainer
def trainer_exercises_list(request):
    trainer = Trainer.objects.get(user__id = request.user.id)
    exercises: list[Exercise] = list(Exercise.objects.filter(trainer = trainer))       
    context = {
        "exercises": exercises,
    }
    return render(request, "pages/trainer_exercise.html", context)



# add new workout
def new_exercise(request):
    form = ExerciseForm()         
    if request.method == "POST":
        form = ExerciseForm(request.POST,request.FILES)
        if form.is_valid():
            exercise =form.save()
            exercise.trainer = request.user.trainer
            print(f" I'm in new: {exercise.slug}")
            exercise.save()
            return redirect("exercises")
    context = {
        "form": form,
    }
    return render(request, "pages/add_exercise.html", context)



# edit workout
def edit_exercise(request, slug):
    exercise = Exercise.objects.get(slug=slug)
    print(exercise.slug)
    form = ExerciseForm(instance=exercise)
    if request.method == "POST":
        form = ExerciseForm(request.POST, request.FILES ,instance=exercise)
        if form.is_valid():
            form.save()
            print(f" I'm in editing: {exercise.slug}")
            return redirect("exercises")
    context = {
        "form": form,
    }
    return render(request, "pages/edit_exercise.html", context)



def delete_exercise(request, slug):
    exercise = Exercise.objects.get(slug=slug)
    exercise.delete()
    return redirect("exercises")
    


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
            return redirect("home")
    context = {
        "forms": forms,
        "trainee":trainee
    }
    return render(request, "pages/assign_exercise.html", context)




########### Subscription ########### 
def trainer_subs_list(request):
    trainer = Trainer.objects.get(user__id = request.user.id)
    subs: list[Subscription] = list(Subscription.objects.filter(trainer = trainer))       
    context = {
        "subs": subs,
    }
    return render(request, "pages/trainer_subscriptions.html", context)



# Subscribers 
def subscribers_list(request):
    trainer = Trainer.objects.get(user__id = request.user.id)
    subsItems: list[SubscriptionItem] = list(SubscriptionItem.objects.filter(plan__trainer = trainer))       
    context = {
        "subsItems": subsItems,
    }
    return render(request, "pages/subscribers.html", context)



# create new subscription plan
def subcription_create_view(request):
    form = TrainerSubscriptionForm()
    if request.method == "POST":
        form = TrainerSubscriptionForm(request.POST)
        if form.is_valid():
            plan=form.save(commit=False)
            plan.trainer = request.user.trainer
            plan.save()
            return redirect("subscriptions")
    context = {
        "form": form,
    }
    return render(request, 'pages/add_subscription.html', context)



# update subscription plan
def subscription_update_view(request):
    subscription = Subscription.objects.get(trainer_id=request.user.id)
    form = TrainerSubscriptionForm(instance=subscription)
    if request.method == "POST":
        form = TrainerSubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect("subscriptions")
    context = {
        "form": form,
    }
    return render(request, 'pages/update_sub.html', context)



# delete subscription plan
def subscription_delete_view(request):
    sub= Subscription.objects.get(trainer_id=request.user.id)
    if sub.trainer == request.user.trainer:
        sub.delete()
    return redirect("subscriptions")



# trainee profile and details 
def trainee_details(request, trainee_id):
    trainee = Trainee.objects.get(user_id=trainee_id)
    sub_item = SubscriptionItem.objects.get(trainee_id=trainee_id)
    context = {
        "trainee": trainee,
        "sub": sub_item,
    }
    return render(request, "pages/trainee_details.html", context)