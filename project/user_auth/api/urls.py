from django.contrib import admin
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('user/', views.UserView.as_view(), name='user'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('add_supporter/', views.AddSupporter.as_view(), name='add_supporter'),
    path('add_ticket/', views.AddTicket.as_view(), name='add_ticket'),
    path('all_tickets/', views.GetAllTickets.as_view(), name='all_ticket'),
    path('all_user_tickets/', views.GetAllTicketsForUser.as_view(), name='all_user_tickets'),
]

