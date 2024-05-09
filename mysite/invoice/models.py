from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
# id automatically created as PK, e.g. Freelance_instance.id
class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=300)
    email = models.CharField(max_length=100, validators=[EmailValidator()])
    contact = models.CharField(max_length=20) 

    def __str__(self):
        return self.name

class Client(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE),
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=300)
    email = models.CharField(max_length=100, validators=[EmailValidator()])
    contact = models.CharField(max_length=20) 

    def __str__(self):
        return self.name
    
class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE),
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE),
    date = models.DateTimeField(default=timezone.now),
    month_ending = models.DateTimeField(),
    services = models.JSONField(),
    total_hours = models.IntegerField(),
    hourly_rate = models.IntegerField(),
    been_paid = models.BooleanField(default=False),
    recurring = models.BooleanField(default=False),

    # below, 1st choice value stored in db, 2nd = human_readable name in forms / templates
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('received', 'Received'),
        ('read', 'Read'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)


class History(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE),
    status = models.CharField(max_length=20)
    date = models.DateTimeField(default=timezone.now)