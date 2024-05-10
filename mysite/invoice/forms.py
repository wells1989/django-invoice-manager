from django import forms
from django.core.exceptions import ValidationError
import re, json
from .models import Client, Invoice, Freelancer

class ClientCreationForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Client
        fields = ['name', 'address', 'email', 'contact']
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        address = cleaned_data.get('address')
        email = cleaned_data.get('email')
        contact = cleaned_data.get('contact')

        if not all([name, address, email, contact]):
            raise ValidationError("All fields are required.")

        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("Please enter a valid email address.")

        return cleaned_data


class InvoiceCreationForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Invoice
        fields = ['client', 'client_name', 'client_address', 'client_email', 'client_contact', 
                  'freelancer_name', 'freelancer_address', 'freelancer_email', 'freelancer_contact', 
                  'date', 'month_ending', 'services', 'total_hours', 'total_charge', 'currency', 'been_paid', 'status']

    def clean(self):
        cleaned_data = super().clean()
        client_name = cleaned_data.get('client_name')
        client_address = cleaned_data.get('client_address')
        client_email = cleaned_data.get('client_email')
        client_contact = cleaned_data.get('client_contact')
        freelancer_name = cleaned_data.get('freelancer_name')
        freelancer_address = cleaned_data.get('freelancer_address')
        freelancer_email = cleaned_data.get('freelancer_email')
        freelancer_contact = cleaned_data.get('freelancer_contact')
        date = cleaned_data.get('date')
        month_ending = cleaned_data.get('month_ending')
        services = cleaned_data.get('services')
        currency = cleaned_data.get('currency')
        total_hours = cleaned_data.get('total_hours')
        total_charge = cleaned_data.get('total_charge')

        if not all([client_name, client_address, client_email, client_contact,
                    freelancer_name, freelancer_address, freelancer_email, freelancer_contact,
                    date, month_ending, services, currency, total_hours, total_charge]):
            raise ValidationError("All fields are required.")

        return cleaned_data

    def clean_services(self):
        services_csv = self.cleaned_data['services']
        services_list = []
        lines = services_csv.split('\n')
        for line in lines:
            service_data = {}
            pairs = line.strip().split(',')
            for pair in pairs:
                key, value = pair.split(':')
                service_data[key.strip()] = value.strip()
            services_list.append(service_data)
        return json.dumps(services_list)