from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RoomSerializer, GuestSerializer, BookingSerializer
from .repositories import RoomRepository, GuestRepository, BookingRepository
from .services import HotelService
from django.db.models import Sum, Count
from .models import Room, Booking, Guest

# Rooms
class RoomListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        return RoomRepository().get_all()

    def perform_create(self, serializer):
        RoomRepository().create(**serializer.validated_data)

class RoomRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer

    def get_object(self):
        obj_id = self.kwargs['pk']
        return RoomRepository().get_by_id(obj_id)

    def perform_update(self, serializer):
        RoomRepository().update(self.kwargs['pk'], **serializer.validated_data)

    def perform_destroy(self, instance):
        RoomRepository().delete(self.kwargs['pk'])


#Guests
class GuestListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = GuestSerializer

    def get_queryset(self):
        return GuestRepository().get_all()

    def perform_create(self, serializer):
        GuestRepository().create(**serializer.validated_data)

class GuestRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GuestSerializer

    def get_object(self):
        return GuestRepository().get_by_id(self.kwargs['pk'])

    def perform_update(self, serializer):
        GuestRepository().update(self.kwargs['pk'], **serializer.validated_data)

    def perform_destroy(self, instance):
        GuestRepository().delete(self.kwargs['pk'])


#Bookings
class BookingListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return BookingRepository().get_all()


class BookingRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer

    def get_object(self):
        return BookingRepository().get_by_id(self.kwargs['pk'])

    def perform_update(self, serializer):
        # if updating dates or room, recompute total
        data = serializer.validated_data
        BookingRepository().update(self.kwargs['pk'], **data)

    def perform_destroy(self, instance):
        BookingRepository().delete(self.kwargs['pk'])


#Report
class HotelReportAPIView(APIView):
    def get(self, request):
        total_rooms = Room.objects.count()
        booked_rooms = Room.objects.filter(is_booked=True).count()
        available_rooms = total_rooms - booked_rooms
        occupancy_rate = (booked_rooms / total_rooms) if total_rooms else 0

        total_revenue = Booking.objects.aggregate(total=Sum('total'))['total'] or 0

        bookings_per_room_qs = Booking.objects.values('room__number').annotate(count=Count('id'))
        bookings_per_room = [
            {'room_number': item['room__number'], 'bookings_count': item['count']}
            for item in bookings_per_room_qs
        ]
        guests_count = Guest.objects.count()

        report = {
            'total_rooms': total_rooms,
            'available_rooms': available_rooms,
            'booked_rooms': booked_rooms,
            'occupancy_rate': occupancy_rate,
            'total_revenue': total_revenue,
            'bookings_per_room': bookings_per_room,
            'guests_count': guests_count,
        }
        return Response(report, status=status.HTTP_200_OK)
