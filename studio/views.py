from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.utils import timezone
import pytz
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
import logging

logger = logging.getLogger(__name__)

# Create your views here.
class ClassList(APIView):
    """GET/classes: List upcoming fitness classes."""
    def get(self, request):
        now = timezone.now()
        tz_param = request.GET.get('tz', 'Asia/Kolkata')
        try:
            user_tz = pytz.timezone(tz_param)
        except Exception:
            raise ValidationError("Invalid timezone string")
        
        classes = Class.objects.filter(datetime__gte=now)
        result = []
        for cls in classes:
            local_dt = cls.datetime.astimezone(user_tz)
            result.append({
                "id":cls.id,
                "name":cls.name,
                "datetime":local_dt.isoformat(),
                "instructor":cls.instructor,
                "available_slots":cls.available_slots
            })
            return Response(result)
        
class BookView(APIView):
    def post(self, request):
        serializer = BookingRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        
        fitness_class = get_object_or_404(Class, pk=data['class_id'])
        if fitness_class.available_slots < 1:
            logger.warning(f"Overbooking attempt for class {fitness_class.id}")
            return Response({'error':'No slots available for this class.'},
                            status=status.HTTP_400_BAD_REQUEST)
            
        fitness_class.available_slots -= 1
        fitness_class.save()
        booking = Booking.objects.create(
            fitness_class=fitness_class,
            client_name=data['client_name'],
            client_email=data['client_email']
        )
        
        logger.info(f"Booking created: {booking}")
        out_serializer = BookingSerializer(booking)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
    
class BookingList(APIView):
    def get(self, request):
        email = request.GET.get('email')
        if not email:
            return Response({'error':'Client email is required as a query parameter.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        bookings = Booking.objects.filter(client_email=email)
        serializer=BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
        
        
            
            
        