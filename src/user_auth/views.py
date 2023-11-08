from django.shortcuts import render
from rest_framework.views import APIView
from . import serializers, models
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

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

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'jwt': token
        }

        return response
    
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('You are not logged in!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('You are not logged in!')
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

class AddSupporter(APIView):
    def post(self, request):
        serializer = serializers.SupporterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class AddTicket(APIView):
    def post(self, request):
        serializer = serializers.TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)