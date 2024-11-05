from django.contrib import admin
from django.urls import path, include

from api.views import hotel_list, add_hotel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    path('hotels/', hotel_list, name='hotel-list'),
    path('add_hotel/', add_hotel, name='add-hotel'),
]
