from datetime import datetime, date
from turtle import done
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
    subs = Subscription.objects.filter(trainer_id=request.user.id).all().count()
    users = SubscriptionItem.objects.filter(plan=request.user.id).all()
    earnng= 0
    for user in users:
        if user.payment_status:
            earnng = earnng+ user.plan.price 
    context = {
        "subs": subs,
        "earnng": earnng,
        "users": users.filter(end_date__gte=datetime.today(),active =True).count(),
    }
    return render(request,'pages/home_page.html', context)


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
            return redirect("home")
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
    # setsFormset = inlineformset_factory(model= ExerciseItem, parent_model=Trainee, form=ExerciseItemForm,extra=0)
    forms = ExerciseItemForm()  
    # for form in forms:
    forms.fields["exercise"].queryset = Exercise.objects.filter(trainer=request.user.trainer)
    
    if request.method == "POST":
        forms = ExerciseItemForm(request.POST)
        if forms.is_valid():
            # for form in forms:
            child = forms.save(commit=False)
            child.trainee = trainee
            child.save()
            return redirect("home")
    context = {
        "forms": forms,
        "trainee":trainee
    }
    return render(request, "pages/assign_exercise.html", context)
def get_form_kwargs(self):
    kwargs = super(assign_exercise, self).get_form_kwargs()
    kwargs['user'] = self.request.user.trainer
    return kwargs 




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
    sub_item = SubscriptionItem.objects.filter(trainee_id=trainee_id, plan__trainer= request.user.trainer).all()
    exercises = ExerciseItem.objects.filter(trainee_id=trainee_id, date__range = [sub_item.start_date,sub_item.end_date],exercise__trainer =request.user.trainer).all()
    labels = [
        "done", 
        "not done",
        ]
    
    data = [
            exercises.filter(done=True).count(),
            exercises.filter(done=False).count(),
            ]
    
    times = 0
    for obj in exercises:
        print(obj.time)
        if obj.done == True:
            times = times + int(obj.time.strftime("%M"))
    
    active_calories = 0
    for exercise in exercises.filter(done=True):
        exerciseCalories = 0
        try:
            exerciseCalories = int(exercise.time.strftime("%M")) * 3 * 3.5 * trainee.weight/200
        except:
            exerciseCalories = 10 * 3 * 3.5 * 70/200
        active_calories = active_calories + exerciseCalories 
    # def sum_of_time(times):
    #     total = time(00, 00, 00)
    #     for val in times:
    #         total.min = total(minutes=val.min)
    #     print(f"look at me I'm the total: {total}")
    #     int.parse(total)
    #     return total
    if sub_item.start_date > date.today() or sub_item.end_date < date.today():
        cant_asaing=True
    else:
        cant_asaing= False
    context = {
        "trainee": trainee,
        "sub": sub_item,
        "exercises": exercises,
        "data": data,
        "labels": labels,
        # "time": sum_of_time(tsimes),
        "time": times,
        "calories": active_calories,
        "cant_assign":cant_asaing
    }
    return render(request, "pages/trainee_details.html", context)