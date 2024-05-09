from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import FreelancerCreationForm
from invoice.models import Freelancer
from django.contrib.auth.views import LoginView
from django.contrib import messages


def register(request):
    if request.user.is_authenticated:
        return redirect('invoice:home')

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

        if form.is_valid():

            freelancer = form.save(commit=False)
            freelancer.user = request.user
            freelancer.save()

            return redirect('invoice:home')
        else:
            return render(request, 'users/setup.html', {'form': form})
        

class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('invoice:home')
        return super().dispatch(request, *args, **kwargs)
    
@login_required
def change_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')

        if len(new_username) < 5:
            messages.error(request, 'Minimum 5 characters.')
            return redirect('invoice:settings')
        
        request.user.username = new_username
        request.user.save()
        messages.success(request, 'Username changed successfully.')

    return redirect('invoice:settings')

@login_required
def change_password(request):
    if request.method == 'POST':

        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        
        user = authenticate(username=request.user.username, password=current_password)
        if user is not None:
            if len(new_password) < 5:
                messages.error(request, 'Minimum 8 characters.')
                return redirect('invoice:settings')

            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password changed successfully.')
        else:
            messages.error(request, 'Incorrect credentials.')

    return redirect('invoice:settings')