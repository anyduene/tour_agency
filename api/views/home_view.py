from django.shortcuts import render
from api.repositories.context import context


def home(request):
    tours = context.tours.get_all()
    return render(request, 'index.html', {'entities': tours})