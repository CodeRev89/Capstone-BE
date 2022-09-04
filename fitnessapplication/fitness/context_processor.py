from .models import Trainer
from .forms import TrainerLogin, TrainerRegister

def processor(request):
    register_form = TrainerRegister()
    login_form = TrainerLogin()
    if request.user.is_authenticated:
        trainer = Trainer.objects.get(user_id=request.user)
        return {
           'register': register_form,
            'login': login_form,
            'trainer': trainer,
        }  
    else: 
        return {
            'register': register_form,
            'login': login_form,
        }
   