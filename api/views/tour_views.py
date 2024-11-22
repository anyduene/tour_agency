from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from api.repositories.context import context
from django.contrib import messages

from api.views.forms import TourForm


@api_view(['GET'])
def tour_list(request):
    tours = context.tours.get_all()
    return render(request, 'tour_list.html', {'entities': tours})

@api_view(['GET'])
def tour_detail(request, tour_id):
    tour = context.tours.get_by_id(tour_id)
    print(context.tours.avg_tour_price())
    return render(request, 'tour_detail.html', {'tour': tour})

@staff_member_required
def add_tour(request):
    if request.method == 'POST':
        form = TourForm(request.POST)
        if form.is_valid():
            context.tours.create(form.cleaned_data)
            return redirect('tour-list')
        else:
            print(form.errors)
    else:
        form = TourForm()

    return render(request, 'add_tour.html', {'form': form})


@staff_member_required
def edit_tour(request, tour_id):
    tour = context.tours.get_by_id(tour_id)

    if request.method == 'POST':
        form = TourForm(request.POST, instance=tour)
        if form.is_valid():
            context.tours.update(tour_id, form.cleaned_data)
            return redirect('tour-detail', tour.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TourForm(instance=tour)

    return render(request, 'edit_tour.html', {'form': form, 'tour': tour})


@staff_member_required
def delete_tour(request, tour_id):
    context.tours.delete(tour_id)
    return redirect('tour-list')