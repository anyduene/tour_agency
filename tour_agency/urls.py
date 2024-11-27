from django.contrib import admin
from django.urls import path, include

from api.views.dashboards_view import dashboard_v1
from api.views.home_view import home
from api.views.hotel_views import hotel_list, add_hotel
from api.views.request_view import item_list, delete_item
from api.views.tour_views import tour_list, tour_detail, add_tour, edit_tour, delete_tour

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    path('home/', home, name='home'),
    path('hotels/', hotel_list, name='hotel-list'),
    path('add_hotel/', add_hotel, name='add-hotel'),

    path('tours/', tour_list, name='tour-list'),
    path('tours/<int:tour_id>/', tour_detail, name='tour-detail'),
    path('add_tour/', add_tour, name='add-tour'),
    path('edit_tour/<int:tour_id>/', edit_tour, name='edit-tour'),
    path('delete_tour/<int:tour_id>/', delete_tour, name='delete-tour'),

    path('requests/', item_list, name='request-list'),
    path('requests/delete/<int:item_id>/', delete_item, name='requests-delete-item'),


    # path('api/dashboard/v2/', dashboard_v2, name='dashboard-v2'),
    path('dashboard/v1/', dashboard_v1, name='dashboard-v1'),
]
