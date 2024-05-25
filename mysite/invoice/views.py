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

        freelancer = Freelancer.objects.get(user=request.user)
    
        # total invoices / clients for top stats
        invoices = Invoice.objects.filter(freelancer=freelancer).order_by('date')
        invoice_count = invoices.count()
        clients = Client.objects.filter(freelancer=freelancer)
        client_count = clients.count()

        # data for charts
        currencies = {}
        client_earnings = {}
        months= {}
        total_earnings = 0

        for invoice in invoices:
            invoice.currency = invoice.currency.upper()
            invoice.client_name = invoice.client_name.lower()
            invoice.total_charge = float(invoice.total_charge)
            
            # total earnings sum
            total_earnings += invoice.total_charge

            # populating currencies dictionary
            if invoice.currency not in currencies.keys():
                currencies[invoice.currency] = 0
            currencies[invoice.currency] += float(invoice.total_charge)

            # populating client_earings dictionary
            if invoice.client_name not in client_earnings.keys():
                client_earnings[invoice.client_name] = {'total': 0, 'currencies': {}}
            
            client_earnings[invoice.client_name]['total'] += invoice.total_charge
            
            if invoice.currency not in client_earnings[invoice.client_name]['currencies'].keys():
                client_earnings[invoice.client_name]['currencies'][invoice.currency] = 0
            
            client_earnings[invoice.client_name]['currencies'][invoice.currency] += invoice.total_charge

            # populating months dictionary
            month = invoice.date.strftime('%Y-%m')
            if not month in months:
                months[month] = {'total': 0, 'paid': 0, 'unpaid': 0}

            months[month]['total'] += invoice.total_charge

            if invoice.been_paid:
                months[month]['paid'] += invoice.total_charge
            else:
                months[month]['unpaid'] += invoice.total_charge

        if invoice_count == 0:
            average_charge = None
        else:
            average_charge = total_earnings / invoice_count

        return render(request, 'invoice/home.html', {'freelancer':freelancer, 'invoice_count': invoice_count, 'client_count': client_count, 'currencies': currencies, 'client_earnings': client_earnings, 'months': months, 'total_earnings': total_earnings, 'average_charge': average_charge})
    

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
            invoice = form.save()
            messages.success(request, 'Invoice successfully added.')

            history = History.objects.create(invoice=invoice, status=invoice.status, been_paid=invoice.been_paid)
        else:
            
            messages.error(request, 'errors occurred with the invoice form')


    return render(request, 'invoice/new_invoice.html', {'freelancer': freelancer, 'clients': clients, 'form': form})


@login_required
def create_client(request):
    if request.method == "POST":
        freelancer = Freelancer.objects.get(user=request.user)
        clients = Client.objects.filter(freelancer=freelancer)
        form = ClientCreationForm(request.POST)

        if form.is_valid():

            client = form.save(commit=False)
            freelancer = Freelancer.objects.get(user=request.user)
            client.freelancer = freelancer
            client.save()
            messages.success(request, 'Client successfully added.')
        else:
            messages.error(request, 'Error occurred.')

        return render(request, 'invoice/new_invoice.html', {'freelancer': freelancer, 'clients': clients, 'form': form})

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

    freelancer = Freelancer.objects.get(user=request.user)
    invoices= Invoice.objects.filter(freelancer=freelancer).order_by('-pk', '-date')
    clients = Client.objects.filter(freelancer=freelancer)

    for invoice in invoices:
        invoice.services = invoice.services.split('\n')
    
    if request.method == "POST":
        start_date_filter = request.POST.get('search_start_date')
        end_date_filter = request.POST.get('search_end_date')
        client_filter = request.POST.get('search_client')
        paid_filter = request.POST.get('search_paid')
        unpaid_filter = request.POST.get('search_unpaid')
        status_filter = request.POST.get('search_status')

        filters = {}

        if start_date_filter:
            filters['date__gte'] = start_date_filter
        
        if end_date_filter:
            filters['date__lte'] = end_date_filter

        if client_filter:
            filters['client__name'] = client_filter

        if paid_filter:
            filters['been_paid'] = True
        elif unpaid_filter:
            filters['been_paid'] = False

        if status_filter:
            filters['status'] = status_filter

        invoices = invoices.filter(**filters)

        if filters:
            filter_string = "Filtering: "
            for key, value in filters.items():
                if "__lte" in key or "__gte" in key:
                    key, operator = key.rsplit('__', 1)

                    print(f'operator = {operator}')
                    symbol = "<=" if operator == "lte" else ">="
                    filter_string += f'{key} {symbol} {value}. '
                else:
                    filter_string += f'{key}: {value}. '
            messages.success(request, filter_string)
        else:
            messages.success(request, "filters cleared")

    return render(request, 'invoice/my_invoices.html', {'invoices': invoices, 'freelancer': freelancer, 'clients': clients})

@login_required
def update_invoice(request, id):

    if request.method == "POST":
        invoice = Invoice.objects.get(pk=id)
        form = InvoiceCreationForm(request.POST, instance=invoice)

        prior_status = invoice.status
        prior_been_paid = invoice.been_paid

        if form.is_valid():
            updated_invoice = form.save()
            messages.success(request, "invoice successfully updated")
            
            if (updated_invoice.status != prior_status or 
                updated_invoice.been_paid != prior_been_paid):

                history = History.objects.create(invoice=updated_invoice)
                
                if updated_invoice.status != prior_status:
                    history.status = updated_invoice.status
                
                if updated_invoice.been_paid != prior_been_paid:
                    history.been_paid = updated_invoice.been_paid

                history.save()
            
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

    freelancer=Freelancer.objects.get(user=request.user)
    invoices = Invoice.objects.filter(freelancer=freelancer)

    history = History.objects.filter(invoice__in=invoices).order_by('-date')
    
    if request.method == "POST":
        tag = request.POST.get('tag')
        if tag is not None:
            history = history.filter(invoice__tag=tag) # __accessing foreign key properties 
            
        invoice_id = request.POST.get('invoice_id')
        if invoice_id:
            invoice = Invoice.objects.get(pk=invoice_id)
            history = history.filter(invoice=invoice)
           
    return render(request, 'invoice/history.html', {'history': history, 'invoices': invoices})


