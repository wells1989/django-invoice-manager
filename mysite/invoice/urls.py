from . import views
from django.urls import path

app_name = 'invoice'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('home/', views.home, name='home'),

    path('settings/', views.settings, name='settings'),
    path('my_invoices/', views.my_invoices, name='my_invoices'),
    path('update_invoice/<int:id>', views.update_invoice, name="update_invoice"),
    path('new_invoice/', views.new_invoice, name='new_invoice'),
    path('new_invoice/create_client', views.create_client, name='create_client'),
    path('history/', views.history, name='history'),
    path('statistics/', views.statistics, name='statistics'),
    path('new_invoice/delete_client/<int:id>', views.delete_client, name="delete_client"),
    path('my_invoices/delete_invoice/<int:id>', views.delete_invoice, name="delete_invoice")
]
