from django.shortcuts import render, redirect
from api.NetworkHelper import NetworkHelper

BASE_URL = 'http://127.0.0.1:8001/'

def item_list(request):
    network_helper = NetworkHelper(BASE_URL)

    response_data = network_helper.get_list()
    items = response_data.get('tours', [])

    return render(request, 'requests.html', {'items': items})


def delete_item(request, item_id):
    network_helper = NetworkHelper(BASE_URL)
    network_helper.delete_item(item_id)
    return redirect('home')