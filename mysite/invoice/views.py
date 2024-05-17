from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import Freelancer, Client, Invoice, History
from django.contrib import messages
from .forms import ClientCreationForm, InvoiceCreationForm
from django.http import JsonResponse
from django.urls import reverse

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

            form.save()
            messages.success(request, 'Invoice successfully added.')
        else:
            
            messages.error(request, 'errors occurred with the invoice form')


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
def delete_client(request, id):
    try:
        client = Client.objects.get(pk=id)

        client.delete()
        messages.success(request, "client successfully deleted")
    except:
        messages.error(request, "error deleting client")

    return redirect(reverse('invoice:new_invoice'))


@login_required
def my_invoices(request):
    if request.method == "GET":
        freelancer = Freelancer.objects.get(user=request.user)
        invoices= Invoice.objects.filter(freelancer=freelancer).order_by('-pk', '-date')
        clients = Client.objects.filter(freelancer=freelancer)

        for invoice in invoices:
            invoice.services = invoice.services.split('\n')

        return render(request, 'invoice/my_invoices.html', {'invoices': invoices, 'freelancer': freelancer, 'clients': clients})
    elif request.method == "PUT":
        pass

@login_required
def update_invoice(request, id):

    if request.method == "POST":
        invoice = Invoice.objects.get(pk=id)
        form = InvoiceCreationForm(request.POST, instance=invoice)

        if form.is_valid():
            form.save()
            messages.success(request, "invoice successfully updated")
            # Optionally add success message
        else:
            messages.error(request, "error in updating the form")

    return redirect(reverse('invoice:my_invoices'))

@login_required
def delete_invoice(request, id):
    try:
        invoice = Invoice.objects.get(pk=id)

        invoice.delete()
        messages.success(request, "invoice successfully deleted")
    except:
        messages.error(request, "error deleting invoice")

    return redirect(reverse('invoice:my_invoices'))


@login_required
def history(request):
    return render(request, 'invoice/history.html')

@login_required
def statistics(request):
    return render(request, 'invoice/statistics.html')

