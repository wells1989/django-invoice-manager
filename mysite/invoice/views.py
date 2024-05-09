from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import Freelancer
from django.contrib import messages

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
    

@login_required
def settings(request):

    if request.method == 'GET':
        freelancer = Freelancer.objects.get(user=request.user)

        return render(request, 'invoice/settings.html', {'freelancer': freelancer})

    elif request.method == 'POST':
        try:
            request.user.freelancer.name = request.POST.get('name')
            request.user.freelancer.address = request.POST.get('address')
            request.user.freelancer.email = request.POST.get('email')
            request.user.freelancer.contact = request.POST.get('contact')
            request.user.freelancer.save()
            messages.success(request, 'Settings updated successfully.')
        except:
            messages.error(request, 'Error Occurred.')

        return redirect('invoice:settings')

@login_required
def my_invoices(request):
    return render(request, 'invoice/my_invoices.html')

@login_required
def new_invoice(request):
    return render(request, 'invoice/new_invoice.html')

@login_required
def history(request):
    return render(request, 'invoice/history.html')

@login_required
def statistics(request):
    return render(request, 'invoice/statistics.html')

