from django.urls import path
from .views import *

urlpatterns = [
    path('rooms/', RoomListCreateAPIView.as_view(), name='rooms-list'),
    path('rooms/<int:pk>/', RoomRetrieveUpdateDeleteAPIView.as_view(), name='rooms-detail'),

    path('guests/', GuestListCreateAPIView.as_view(), name='guests-list'),
    path('guests/<int:pk>/', GuestRetrieveUpdateDeleteAPIView.as_view(), name='guests-detail'),

    path('bookings/', BookingListCreateAPIView.as_view(), name='bookings-list'),
    path('bookings/<int:pk>/', BookingRetrieveUpdateDeleteAPIView.as_view(), name='bookings-detail'),

    path('report/', HotelReportAPIView.as_view(), name='hotel-report'),
]