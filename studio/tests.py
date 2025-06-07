from django.test import TestCase
from rest_framework.test import APIClient
from django.utils import timezone
from .models import *
from django.urls import reverse
from rest_framework import status


# Create your tests here.
class BookingAPITestCase(TestCase):
    def setUp(self):
        self.client=APIClient()
        self.future_time = timezone.now() + timezone.timedelta(days=1)
        self.fitness_class = Class.objects.create(
            name='Yoga',
            datetime=self.future_time,
            instructor='John',
            available_slots=2
        )
        
    def test_get_classes(self):
        response = self.client.get(reverse('class-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['name'], 'Yoga')
        
    def test_successful_booking(self):
        data={
            'class_id':self.fitness_class.id,
            'client_name':'Bobby lashley',
            'client_email':'bobby@xyz.com'
        }
        response = self.client.post(reverse('book'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # To verify slots is decrement or not
        self.fitness_class.refresh_from_db()
        self.assertEqual(self.fitness_class.available_slots, 1)
        
        # Booking should be created
        booking = Booking.objects.get(client_email='bobby@xyz.com')
        self.assertEqual(booking.client_name, 'Bobby lashley')
        
    # To test over booking
    def test_overbooking(self):
        self.fitness_class.available_slots = 0
        self.fitness_class.save()
        data={
            'class_id':self.fitness_class.id,
            'client_name':'rollins',
            'client_email':'rollins@xyz.com'
        }
        response = self.client.post(reverse('book'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No slots available', response.data.get('error',''))
        
    # Test missing fields
    def test_missing_fields(self):
        data = {'class_id': self.fitness_class.id, 
                'client_name':'Dean'
                }
        response = self.client.post(reverse('book'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    # Test booking by email
    def test_get_bookings_by_email(self):
        bookings = Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name='Evy',
            client_email='evy@xyz.com'
        )
        url = f"{reverse('bookings')}?email=evy@xyz.com"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['client_name'], 'Evy')
        
    # Test if no email
    def test_bookings_no_email(self):
        response = self.client.get(reverse('bookings'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
        