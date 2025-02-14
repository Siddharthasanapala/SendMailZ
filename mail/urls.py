from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send-mails/', views.send_mails, name='send_mails'),
]