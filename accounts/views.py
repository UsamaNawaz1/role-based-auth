from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# Create your views here.


def home(request):
    return render(request, 'accounts/login.html')

def loginPage(request):
    data = dict()
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            
            messages.error(request, "username or password is incorrect")
 
    
    return render(request, 'accounts/login.html', data)

@login_required(login_url='home')
def dashboard(request):
    users = User.objects.all()
    total_users = users.count() - 1
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.email = request.POST.get('email')
            user.save()
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            userprofile = UserProfile.objects.create(user = user, first_name=first_name, last_name=last_name)
            userprofile.save()
    else:
        form = UserCreationForm()
    context = {
        'users':users,
        'total_users': total_users
    }
    return render(request, 'accounts/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.email = request.POST.get('email')
            user.save()
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            userprofile = UserProfile.objects.create(user = user, first_name=first_name, last_name=last_name)
            userprofile.save()
        
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form':form})


@login_required(login_url='home')
def logoutPage(request):
    logout(request)
    return redirect('home')