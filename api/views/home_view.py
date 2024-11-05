from django.shortcuts import render
from api.services.tour_service import TourService


def home(request):
    tours = TourService.get_all_tours()
    return render(request, 'index.html', {'entities': tours})