from .repositories import RoomRepository, GuestRepository, BookingRepository
from datetime import date

class HotelService:
    def __init__(self):
        self.rooms = RoomRepository()
        self.guests = GuestRepository()
        self.bookings = BookingRepository()

    def book_room(self, guest_id, room_id, check_in, check_out):
        guest = self.guests.get_by_id(guest_id)
        room = self.rooms.get_by_id(room_id)
        nights = (check_out - check_in).days
        total = nights * room.price

        booking = self.bookings.create(
            guest=guest, room=room,
            check_in=check_in, check_out=check_out, total=total
        )
        room.is_booked = True
        room.save()
        return booking
