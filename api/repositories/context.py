from api.repositories.tour_repository import TourRepository
from api.repositories.hotel_repository import HotelRepository
from api.repositories.transport_repository import TransportRepository

class Context:
    def __init__(self):
        self.tours = TourRepository()
        self.hotels = HotelRepository()
        self.transports = TransportRepository()

context = Context()