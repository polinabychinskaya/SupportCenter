from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class SupporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Supporter
        fields = ['id', 'user', 'status']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tickets
        fields = ['id', 'sender', 'supporter', 'description', 'created_at', 'updated_at', 'status']