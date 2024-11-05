from ..models import Tour
from ..repositories.repository import Repository
from ..serializers.tour_serializer import TourSerializer


class TourService:
    rep = Repository(Tour)

    @staticmethod
    def create_tour(data):
        return TourService.rep.create(**data)

    @staticmethod
    def get_all_tours():
        tours = TourService.rep.all()
        serializer = TourSerializer(tours, many=True)
        return serializer.data

    @staticmethod
    def get_tour_by_id(tour_id):
        return TourService.rep.get(tour_id)

    @staticmethod
    def delete_tour(tour_id):
        tour = TourService.rep.get(tour_id)
        if tour:
            TourService.rep.delete(tour)
            return True
        return False
