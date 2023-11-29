from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.http import HttpResponse
from . import models
from rest_framework.response import Response
from django.urls import reverse

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('jwt')
        if request.path == reverse('api:login'):
            response = self.get_response(request)
            return response
        if not token:
            return HttpResponse('Unauthorized', status=401)
        response = self.get_response(request)
        return response
 
