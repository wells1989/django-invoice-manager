from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
# id automatically created as PK, e.g. Freelance_instance.id
class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=300)
    email = models.CharField(max_length=100, validators=[EmailValidator()])
    contact = models.CharField(max_length=20) 

    def __str__(self):
        return self.name

class Client(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=300)
    email = models.CharField(max_length=100, validators=[EmailValidator()])
    contact = models.CharField(max_length=20) 

    def __str__(self):
        return self.name
    
class Invoice(models.Model):
    client = models.ForeignKey(Client, default=None, on_delete=models.SET_DEFAULT)
    # Denormalized fields from Client model (in case they change in the future)
    client_name = models.CharField(max_length=50, default=None)
    client_address = models.CharField(max_length=300, default=None)
    client_email = models.CharField(max_length=100, validators=[EmailValidator()], default=None)
    client_contact = models.CharField(max_length=20, default=None)

    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    # Denormalized fields from Freelancer model
    freelancer_name = models.CharField(max_length=50, default=None)
    freelancer_address = models.CharField(max_length=300, default=None)
    freelancer_email = models.CharField(max_length=100, validators=[EmailValidator()], default=None)
    freelancer_contact = models.CharField(max_length=20, default=None)

    date = models.DateTimeField(default=timezone.now)
    month_ending = models.DateTimeField(default=None)
    services = models.TextField(null=True)
    total_hours = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_charge = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    currency = models.CharField(max_length=3, default="EUR")
    been_paid = models.BooleanField(default=False)

    # below, 1st choice value stored in db, 2nd = human_readable name in forms / templates
    STATUS_CHOICES = [
        ('ready', 'Ready'),
        ('sent', 'Sent'),
        ('received', 'Received'),
        ('read', 'Read'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Ready")


class History(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    been_paid = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)