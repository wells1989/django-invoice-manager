from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import FreelancerCreationForm
from invoice.models import Freelancer


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('users:setup')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def setup(request):
    if request.method == 'GET':
        form = FreelancerCreationForm()
    
        return render(request, 'users/setup.html', {'form': form})

    elif request.method == 'POST':
        form = FreelancerCreationForm(request.POST)

        print(request.POST)
        if form.is_valid():

            freelancer = form.save(commit=False)
            freelancer.user = request.user
            freelancer.save()

            return redirect('invoice:home')
        else:
            return render(request, 'users/setup.html', {'form': form})