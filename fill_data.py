import os
import django
import random
from datetime import date, timedelta

# Налаштування оточення Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_booking.settings')
django.setup()

from hotel.models import Booking, Room, Guest


def reset_and_populate_hotel(booking_count=70):
    print("Cleaning database...")
    Booking.objects.all().delete()
    Room.objects.all().delete()
    Guest.objects.all().delete()

    room_types = ['Standard', 'Double', 'Family', 'Suite', 'VIP']
    all_rooms = []

    for floor in range(1, 6):
        for room_num in range(1, 10):
            number = int(f"{floor}0{room_num}")
            room = Room.objects.create(
                number=number,
                room_type=random.choice(room_types),
                price=float(floor * 50.0 + random.randint(50, 150)),
                is_booked=False
            )
            all_rooms.append(room)

    booked_rooms = random.sample(all_rooms, 38)
    for room in booked_rooms:
        room.is_booked = True
        room.save()

    f_names = ["John", "Jane", "Alex", "Emily", "Chris", "Katie", "Brian", "Sarah", "Mark", "Olivia"]
    l_names = ["Smith", "Doe", "Wilson", "Brown", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris"]

    guests = []
    for i in range(60):
        name = f"{random.choice(f_names)} {random.choice(l_names)} #{i + 1}"
        guest = Guest.objects.create(name=name)
        guests.append(guest)

    today = date(2025, 12, 29)
    year_start = date(2025, 1, 1)
    print(f"Generating {booking_count} bookings for the year 2025...")

    for room in booked_rooms:
        guest = random.choice(guests)
        stay_duration = random.randint(1, 14)
        check_in = today - timedelta(days=random.randint(0, stay_duration - 1))
        check_out = check_in + timedelta(days=stay_duration)

        Booking.objects.create(
            guest=guest,
            room=room,
            check_in=check_in,
            check_out=check_out
        )

    remaining_count = max(0, booking_count - 38)
    for _ in range(remaining_count):
        room = random.choice(all_rooms)
        guest = random.choice(guests)
        check_in = year_start + timedelta(days=random.randint(0, 350))
        duration = random.randint(1, 14)
        check_out = check_in + timedelta(days=duration)

        Booking.objects.create(
            guest=guest,
            room=room,
            check_in=check_in,
            check_out=check_out
        )

    print(f"Done!")

if __name__ == '__main__':
    reset_and_populate_hotel(70)