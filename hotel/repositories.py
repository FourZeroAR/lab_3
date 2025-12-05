from .models import Room, Guest, Booking

class BaseRepository:
    model = None

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, obj_id):
        return self.model.objects.get(id=obj_id)

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, obj_id):
        return self.model.objects.get(id=obj_id)

    def create(self, **kwargs):
        obj = self.model.objects.create(**kwargs)
        return obj

    def update(self, obj_id, **kwargs):
        obj = self.get_by_id(obj_id)
        for k, v in kwargs.items():
            setattr(obj, k, v)
        obj.save()
        return obj

    def delete(self, obj_id):
        obj = self.get_by_id(obj_id)
        obj.delete()
        return True

class RoomRepository(BaseRepository):
    model = Room


class GuestRepository(BaseRepository):
    model = Guest


class BookingRepository(BaseRepository):
    model = Booking
