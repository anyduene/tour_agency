from api.repositories.tour_repository import TourRepository
from api.repositories.hotel_repository import HotelRepository

class Context:
    def __init__(self):
        self.tours = TourRepository()
        self.hotels = HotelRepository()

context = Context()