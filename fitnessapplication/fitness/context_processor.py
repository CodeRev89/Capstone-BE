from .models import Trainer
from .forms import TrainerLogin, TrainerRegister

def processor(request):
    register_form = TrainerRegister()
    login_form = TrainerLogin()
    trainer = Trainer.objects.get(user_id=request.user)
    if  request.user.is_trainer:
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
   