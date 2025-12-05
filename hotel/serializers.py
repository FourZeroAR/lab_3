from rest_framework import serializers
from .models import Room, Guest, Booking

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'number', 'room_type', 'price', 'is_booked']

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['id', 'name']

class BookingSerializer(serializers.ModelSerializer):
    guest = GuestSerializer(read_only=True)
    guest_id = serializers.IntegerField(write_only=True, required=True)
    room = RoomSerializer(read_only=True)
    room_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Booking
        fields = ['id', 'guest', 'guest_id', 'room', 'room_id', 'check_in', 'check_out', 'total']
        read_only_fields = ['total']

    def create(self, validated_data):
        guest_id = validated_data.pop('guest_id')
        room_id = validated_data.pop('room_id')
        from .repositories import GuestRepository, RoomRepository, BookingRepository

        guest = GuestRepository().get_by_id(guest_id)
        room = RoomRepository().get_by_id(room_id)

        check_in = validated_data.get('check_in')
        check_out = validated_data.get('check_out')
        nights = (check_out - check_in).days
        total = nights * room.price

        booking = BookingRepository().create(
            guest=guest,
            room=room,
            check_in=check_in,
            check_out=check_out,
            total=total
        )
        room.is_booked = True
        room.save()
        return booking
