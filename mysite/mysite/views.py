from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


def root(request):
    if request.user.is_authenticated:
        return redirect('invoice:home')
    else:
        return redirect('users:login')
