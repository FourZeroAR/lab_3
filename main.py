import os
import django
from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel_booking.settings")
django.setup()

from hotel.services import HotelService
from hotel.models import Room, Guest, Booking


Room.objects.all().delete()
Guest.objects.all().delete()
Booking.objects.all().delete()

service = HotelService()

room1 = service.rooms.create(number=101, room_type="Single", price=70)
room2 = service.rooms.create(number=201, room_type="VIP",price=150)
room3 = service.rooms.create(number=301, room_type="Suite",price=120)
guest1 = service.guests.create(name="Danylo Kolbasyuk")
guest2 = service.guests.create(name="Ruslan Doroschuk")

booking1 = service.book_room(
    guest_id=guest1.id,
    room_id=room3.id,
    check_in=date(2025, 10, 12),
    check_out=date(2025, 10, 15)
)

booking2 = service.book_room(
    guest_id=guest2.id,
    room_id=room2.id,
    check_in=date(2025, 10, 20),
    check_out=date(2025, 10, 25)
)

print("Booking created:", booking1, booking2)
print("All rooms:")
for room in service.rooms.get_all():
    print(room)

room_ids = [room1.id, room2.id, room3.id]
for rid in room_ids:
    room = service.rooms.get_by_id(rid)
    print(f"Room by ID {rid}:", room)


