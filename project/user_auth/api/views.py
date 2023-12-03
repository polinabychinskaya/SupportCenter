from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from . import serializers
from .. import models
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from rest_framework import generics
from django.http import HttpResponse
import os

# Create your views here.

class Register(APIView):
    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = models.User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('The user is not found!')
        
        payload = {
            'id': user.id,
            #date of token expiry
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            #date of token creation
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, str(os.getenv('SECRET')), algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'jwt': token
        }

        return response
    
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, str(os.getenv('SECRET')), algorithms=['HS256'])
        user = models.User.objects.filter(id=payload['id']).first()
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)
    
class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class SupportersViewSet(viewsets.ModelViewSet):
    queryset = models.Supporter.objects.all()
    serializer_class = serializers.SupporterSerializer

class TicketsViewSet(viewsets.ModelViewSet):
    queryset = models.Tickets.objects.all()
    serializer_class = serializers.TicketSerializer
    def create(self, request):
        serializer = serializers.TicketSerializer(data=request.data)
        token = self.request.COOKIES.get('jwt')
        payload = jwt.decode(token, str(os.getenv('SECRET')), algorithms=['HS256'])
        user = models.User.objects.filter(id=payload['id']).first()
        request.data['sender'] = user.id
        supporter = models.Supporter.objects.filter(status="Available").first()
        request.data['supporter'] = supporter.id
        supporter.status = 'Processing'
        supporter.save()
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
     

class GetAllTicketsForUser(generics.ListAPIView):
    serializer_class = serializers.TicketSerializer
    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')
        payload = jwt.decode(token, str(os.getenv('SECRET')), algorithms=['HS256'])
        user = models.User.objects.filter(id=payload['id']).first()
        queryset = models.Tickets.objects.filter(sender=user)
        return queryset

