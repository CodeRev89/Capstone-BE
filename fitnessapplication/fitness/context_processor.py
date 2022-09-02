from .forms import TrainerLogin, TrainerRegister

def processor(request):
    register_form = TrainerRegister()
    login_form = TrainerLogin()
    
    return {
        'register': register_form,
        'login': login_form,
    }