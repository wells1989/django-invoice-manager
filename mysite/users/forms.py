from django import forms
from django.core.exceptions import ValidationError
import re
from invoice.models import Freelancer

class FreelancerCreationForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Freelancer
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