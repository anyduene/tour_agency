from api.models import Tour
from api.repositories.base_repository import BaseRepository
from api.serializers.tour_serializer import TourSerializer


class TourRepository:
    def __init__(self):
        self.repository = BaseRepository(Tour)

    def create(self, data):
        return self.repository.create(**data)

    def update(self, tour_id, data):
        tour = self.repository.get(tour_id)
        if tour:
            return self.repository.update(tour, **data)
        return None

    def get_all(self):
        tours = self.repository.all()
        serializer = TourSerializer(tours, many=True)
        return serializer.data

    def get_by_id(self, tour_id):
        return self.repository.get(tour_id)

    def delete(self, tour_id):
        tour = self.repository.get(tour_id)
        if tour:
            self.repository.delete(tour)
            return True
        return False
