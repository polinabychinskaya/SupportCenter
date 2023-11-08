from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.Register.as_view()),
    path('login', views.Login.as_view()),
    path('user', views.UserView.as_view()),
    path('logout', views.Logout.as_view()),
    path('add_supporter', views.AddSupporter.as_view()),
    path('add_ticket', views.AddTicket.as_view()),
]

