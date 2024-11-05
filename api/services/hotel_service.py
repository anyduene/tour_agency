from ..models import Hotel
from ..repositories.repository import Repository
from ..serializers.hotel_serializer import HotelSerializer


class HotelService:
    rep = Repository(Hotel)

    @staticmethod
    def create_hotel(data):
        return HotelService.rep.create(**data)

    @staticmethod
    def get_all_hotels():
        hotels = HotelService.rep.all()
        serializer = HotelSerializer(hotels, many=True)
        return serializer.data

    @staticmethod
    def get_hotel_by_id(hotel_id):
        return HotelService.rep.get(hotel_id)

    @staticmethod
    def delete_hotel(hotel_id):
        hotel = HotelService.rep.get(hotel_id)
        if hotel:
            HotelService.rep.delete(hotel)
            return True
        return False
