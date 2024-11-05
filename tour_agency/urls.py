from django.contrib import admin
from django.urls import path, include

from api.views.home_view import home
from api.views.hotel_views import hotel_list, add_hotel
from api.views.tour_views import tour_list, tour_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    path('home/', home, name='home'),
    path('hotels/', hotel_list, name='hotel-list'),
    path('add_hotel/', add_hotel, name='add-hotel'),

    path('tours/', tour_list, name='tour-list'),
    path('tours/<int:tour_id>/', tour_detail, name='tour-detail'),
]
