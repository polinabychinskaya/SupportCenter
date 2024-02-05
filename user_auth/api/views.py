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
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings
from .tasks import email_by_completion

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
    @method_decorator(cache_page(30))
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

    @method_decorator(cache_page(30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class TicketsViewSet(viewsets.ModelViewSet):
    CACHE_KEY_PREFIX = "tickets_view"

    queryset = models.Tickets.objects.all()
    serializer_class = serializers.TicketSerializer

    # Cache key prefixing is a technique used in Django to add a prefix 
    # to the cache keys before storing or retrieving data from the cache. 
    # This prefix is usually based on the name of the cache backend and 
    # allows for creating unique cache keys for different parts of the application.
    @method_decorator(cache_page(60, key_prefix=CACHE_KEY_PREFIX))
    def list(self, request):
        queryset = models.Tickets.objects.select_related('sender').all()
        serializer = serializers.TicketSerializer(queryset, many=True)
        for ticket in serializer.data:
            sender_id = ticket['sender']
            for ticket_item in queryset:
                if ticket_item.sender.pk == sender_id:
                    ticket['sender'] = ticket_item.sender.email
                    break
        return Response(serializer.data)


    def create(self, request):
        serializer = serializers.TicketSerializer(data=request.data)
        token = self.request.COOKIES.get('jwt')
        payload = jwt.decode(token, str(os.getenv('SECRET')), algorithms=['HS256'])
        user = models.User.objects.filter(id=payload['id']).first()
        request.data['sender'] = user.id
        count = models.Supporter.objects.values_list('count', flat=True)
        min_count = min(count)
        supporter = models.Supporter.objects.filter(count=min_count).first()
        request.data['supporter'] = supporter.id
        supporter.count += 1
        supporter.save()
        serializer.is_valid(raise_exception=True)
        serializer.save()
        delete_cache(self.CACHE_KEY_PREFIX)
        return Response(serializer.data)
    
    # PUT - replaces the whole record
    # PATCH - partial modifications to the record
    def partial_update(self, request, *args, **kwargs):
        delete_cache(self.CACHE_KEY_PREFIX)
        ticket = self.get_object()
        data = request.data
        if ticket.response != data.get('response'):
            ticket.response = data.get('response', ticket.response)
            ticket.status = 'Done'
            ticket.save() 
        serializer = self.get_serializer(ticket)
        if serializer.data['status'] == 'Done':
            id = serializer.data['supporter']
            supporter = models.Supporter.objects.filter(id=id).first()
            supporter.count -= 1
            supporter.save()
            sender = models.User.objects.filter(id = serializer.data['sender']).first()
            email_by_completion.delay(to_email=sender.email)
        return Response(serializer.data)

class GetAllTicketsForUser(generics.ListAPIView):
    serializer_class = serializers.TicketSerializer
    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')
        payload = jwt.decode(token, str(os.getenv('SECRET')), algorithms=['HS256'])
        user = models.User.objects.filter(id=payload['id']).first()
        queryset = models.Tickets.objects.filter(sender=user)
        return queryset
    
    @method_decorator(cache_page(30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

def delete_cache(key_prefix: str):
    # Pattern is used to construct a cache key pattern 
    # for cache invalidation or deletion (the way Redis 
    # db stores responses is by creating a pattern (key) to response?)
    keys_pattern = f"views.decorators.cache.cache_*.{key_prefix}.*.{settings.LANGUAGE_CODE}.{settings.TIME_ZONE}"
    cache.delete_pattern(keys_pattern)