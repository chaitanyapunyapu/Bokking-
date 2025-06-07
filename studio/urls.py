from django.urls import path, include
from .views import *

urlpatterns = [
    path('classes/', ClassList.as_view(), name='class-list'),
    path('book/', BookView.as_view(), name='book'),
    path('bookings/', BookingList.as_view(), name='bookings'),
    
]
