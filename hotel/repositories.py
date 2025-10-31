from .models import Room, Guest, Booking

class BaseRepository:
    model = None

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, obj_id):
        return self.model.objects.get(id=obj_id)

    def create(self, **kwargs):
        obj = self.model.objects.create(**kwargs)
        obj.save()
        return obj


class RoomRepository(BaseRepository):
    model = Room


class GuestRepository(BaseRepository):
    model = Guest


class BookingRepository(BaseRepository):
    model = Booking
