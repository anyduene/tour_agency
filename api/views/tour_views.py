from django.shortcuts import render
from rest_framework.decorators import api_view
from api.repositories.context import context

@api_view(['GET'])
def tour_list(request):
    tours = context.tours.get_all()
    return render(request, 'tour_list.html', {'entities': tours})

@api_view(['GET'])
def tour_detail(request, tour_id):
    tour = context.tours.get_by_id(tour_id)
    return render(request, 'tour_detail.html', {'tour': tour})

# @staff_member_required
# def add_tour(request):
#     if request.method == 'POST':
#         data = {
#
#         }
#         TourService.create_tour(data)
#         return redirect('tour-list')
#     return render(request, 'add_tour.html')

# @staff_member_required
# def delete_entity(request, id):
#     if request.method == 'POST':
#         success = TourService.delete_tour(id)
#         if success:
#             return redirect('tour-list')
#         else:
#             return render(request, 'error.html', {'message': 'Hotel not found'})
