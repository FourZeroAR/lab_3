from django.db import models
from datetime import date

class Room(models.Model):
    number = models.IntegerField(unique=True)
    room_type = models.CharField(max_length=50)
    price = models.FloatField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        status = "Booked" if self.is_booked else "Available"
        return f"Room {self.number} ({self.room_type}) - {status}, ${self.price}"


class Guest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.check_in and self.check_out:
            delta = self.check_out - self.check_in
            days = delta.days
            if days <= 0:
                days = 1
            self.total = float(days) * self.room.price

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest} booked room {self.room.number} (${self.total})"
