from django.db import models

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
    total = models.FloatField()

    def __str__(self):
        return f"{self.guest} booked room {self.room.number} (${self.total})"
