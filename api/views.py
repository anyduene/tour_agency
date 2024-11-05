from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services.hotel_service import HotelService

@api_view(['GET'])
def hotel_list(request):
    hotels = HotelService.get_all_hotels()
    return render(request, 'hotel_list.html', {'entities': hotels, 'entity_name': 'Hotels'})

def hotel_detail(request, hotel_id):
    hotel = HotelService.get_hotel_by_id(hotel_id)
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
        HotelService.create_hotel(data)
        return redirect('hotel-list')
    return render(request, 'add_hotel.html')

@staff_member_required
def delete_entity(request, id):
    if request.method == 'POST':
        success = HotelService.delete_hotel(id)
        if success:
            return redirect('hotel-list')
        else:
            return render(request, 'error.html', {'message': 'Hotel not found'})
