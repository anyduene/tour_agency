from django.db.models import Count, Avg, Sum
import pandas as pd
from django.http import JsonResponse, HttpResponse

from api.models import Tour
from api.repositories.base_repository import BaseRepository
from api.serializers.tour_serializer import TourSerializer
from django.db.models.functions import TruncMonth


class TourRepository:
    def __init__(self):
        self.repository = BaseRepository(Tour)

    def create(self, data):
        return self.repository.create(**data)

    def update(self, tour_id, data):
        tour = self.repository.get(tour_id)
        if tour:
            return self.repository.update(tour, **data)
        return None

    def get_all(self):
        tours = self.repository.all()
        serializer = TourSerializer(tours, many=True)
        return serializer.data

    def get_by_id(self, tour_id):
        return self.repository.get(tour_id)

    def delete(self, tour_id):
        tour = self.repository.get(tour_id)
        if tour:
            self.repository.delete(tour)
            return True
        return False



    def tours_by_country(self):
        tours_by_country = Tour.objects.values('destination_country').annotate(
            total_tours=Count('id')
        ).order_by('-total_tours')

        df = pd.DataFrame(list(tours_by_country))
        return df


    def avg_tour_price(self):
        avg_tour_price = Tour.objects.values('destination_country').annotate(
            avg_price=Avg('price')
        ).order_by('-avg_price')

        df = pd.DataFrame(list(avg_tour_price))
        return df


    def tours_with_conditions(self, avg_price_more_than, total_tours_more_than):
        tours = Tour.objects.values('destination_country').annotate(
            total_tours=Count('id'),
            avg_price=Avg('price')
        ).filter(
            total_tours__gt=total_tours_more_than,
            avg_price__gt=avg_price_more_than
        ).order_by('-total_tours')

        df = pd.DataFrame(list(tours))
        return df

    def tours_summary(self):
        summary = Tour.objects.select_related('hotel_booking', 'transport_booking') \
            .values('destination_country') \
            .annotate(total_tours=Count('id'),
                      total_price=Sum('price')) \
            .order_by('-total_tours')

        df = pd.DataFrame(list(summary))
        return df

    def tours_per_month_by_country(self, country):
        tours_by_month = Tour.objects.filter(destination_country=country) \
            .annotate(month=TruncMonth('start_date')) \
            .values('month') \
            .annotate(total_tours=Count('id')) \
            .order_by('month')

        df = pd.DataFrame(list(tours_by_month))
        df['month'] = pd.to_datetime(df['month'])

        full_months = pd.date_range('2024-01-01', '2024-12-01', freq='MS')
        full_months_df = pd.DataFrame(full_months, columns=['month'])
        full_months_df['month'] = pd.to_datetime(full_months_df['month'])

        df = pd.merge(full_months_df, df, how='left', on='month')
        df['total_tours'] = df['total_tours'].fillna(0).astype(int)
        return df


