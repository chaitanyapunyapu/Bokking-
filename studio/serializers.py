from rest_framework import serializers
from .models import *

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name', 'datetime', 'instructor', 'available_slots']
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'fitness_class', 'client_name', 'client_email', 'booked_at']
        
class BookingRequestSerializer(serializers.Serializer):
    class_id = serializers.IntegerField()
    client_name = serializers.CharField(max_length=100)
    client_email = serializers.EmailField()