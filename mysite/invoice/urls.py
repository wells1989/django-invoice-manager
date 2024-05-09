from . import views
from django.urls import path

app_name = 'invoice'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('home/', views.home, name='home'),
]
