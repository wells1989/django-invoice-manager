from django.contrib import admin
from .models import Freelancer, Client, Invoice, History

# Register your models here.
admin.site.register(Freelancer)
admin.site.register(Client)
admin.site.register(Invoice)
admin.site.register(History)
