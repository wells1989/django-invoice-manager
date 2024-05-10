from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import Freelancer, Client, Invoice, History
from django.contrib import messages
from .forms import ClientCreationForm, InvoiceCreationForm
from django.http import JsonResponse

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
def new_invoice(request):
    freelancer = Freelancer.objects.get(user=request.user)
    clients = Client.objects.filter(freelancer=freelancer)
    form = InvoiceCreationForm()

    if request.method == "POST":
        form = InvoiceCreationForm(request.POST)
        if form.is_valid():
            print("valid form")
            form.save()
            messages.success(request, 'Invoice successfully added.')
        else:
            print("invalid form")
            messages.error(request, 'Error in invoice.')

    return render(request, 'invoice/new_invoice.html', {'freelancer': freelancer, 'clients': clients, 'form': form})


@login_required
def create_client(request):
    if request.method == "POST":
        form = ClientCreationForm(request.POST)

        if form.is_valid():

            client = form.save(commit=False)
            freelancer = Freelancer.objects.get(user=request.user)
            client.freelancer = freelancer
            client.save()
            messages.success(request, 'Client successfully added.')
        else:
            messages.error(request, 'Error occurred.')

        return render(request, 'invoice/new_invoice.html', {'form': form})

@login_required
def my_invoices(request):
    return render(request, 'invoice/my_invoices.html')

@login_required
def history(request):
    return render(request, 'invoice/history.html')

@login_required
def statistics(request):
    return render(request, 'invoice/statistics.html')

