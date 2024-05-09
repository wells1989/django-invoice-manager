from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import Freelancer

# Create your views here.
def test(request):
    return HttpResponse("test view working")

@login_required
def home(request):
    if request.user.is_authenticated:
        try:
            logged_in_freelancer = Freelancer.objects.get(user=request.user)
        
            return render(request, 'invoice/home.html', {'logged_in_freelancer':logged_in_freelancer})
        except:
            return redirect('users:login')   
    else:
        return redirect('users:login')


