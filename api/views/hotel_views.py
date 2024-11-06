from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from api.repositories.hotel_repository import HotelRepository

@api_view(['GET'])
def hotel_list(request):
    hotels = HotelRepository.get_all()
    return render(request, 'hotel_list.html', {'entities': hotels})

def hotel_detail(request, hotel_id):
    hotel = HotelRepository.get_by_id(hotel_id)
    return render(request, 'hotel_detail.html', {'hotel': hotel})

@staff_member_required
def add_hotel(request):
    if request.method == 'POST':
        data = {
            'name': request.POST['name'],
            'address': request.POST['address'],
            'city': request.POST['city'],
            'country': request.POST['country'],
            'star_rating': request.POST['star_rating'],
            'mobile_phone': request.POST['mobile_phone'],
            'site': request.POST['site']
        }
        HotelRepository.create(data)
        return redirect('hotel-list')
    return render(request, 'add_hotel.html')

@staff_member_required
def delete_entity(request, id):
    if request.method == 'POST':
        success = HotelRepository.delete(id)
        if success:
            return redirect('hotel-list')
        else:
            return render(request, 'error.html', {'message': 'Hotel not found'})
