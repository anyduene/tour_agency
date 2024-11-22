from api.models import Hotel
from api.repositories.base_repository import BaseRepository
from api.serializers.hotel_serializer import HotelSerializer


class HotelRepository:
    def __init__(self):
        self.repository = BaseRepository(Hotel)

    def create(self, data):
        return self.repository.create(**data)

    def get_all(self):
        hotels = self.repository.all()
        serializer = HotelSerializer(hotels, many=True)
        return serializer.data

    def get_by_id(self, hotel_id):
        return self.repository.get(hotel_id)

    def delete(self, hotel_id):
        hotel = self.repository.get(hotel_id)
        if hotel:
            self.repository.delete(hotel)
            return True
        return False



