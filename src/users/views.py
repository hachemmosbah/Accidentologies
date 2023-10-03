from django.shortcuts import  render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username= username, password=password) 
        if user is not None: 
            login(request, user)
            return redirect('data') 
        else:
            messages.success(request, ('Username ou mot de passe incorrect'))
            return redirect('login')
    else:
        return render(request, 'users/login.html')
   

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        user = User.objects.create_user(name, email, password)
        user.first_name = name
        user.save()
        return render(request, 'users/login.html')
    else:
        return render(request, 'users/signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')
    