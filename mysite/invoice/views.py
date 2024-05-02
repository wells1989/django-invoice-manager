from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def test(request):
    return HttpResponse("test view working")

@login_required
def home(request):
    return render(request, 'invoice/home.html')


