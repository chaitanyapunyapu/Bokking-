from django.db import models

# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    available_slots = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.name} on {self.datetime} with {self.instructor}"
    
class Booking(models.Model):
    fitness_class = models.ForeignKey(Class, related_name='bookings', on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking for {self.client_name} ({self.client_email})"
    