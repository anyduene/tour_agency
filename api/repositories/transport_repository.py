import pandas as pd
from django.db.models import Count

from api.models import Transport
from api.repositories.base_repository import BaseRepository
from api.serializers.transport_serializer import TransportSerializer


class TransportRepository:

    def __init__(self):
        self.repository = BaseRepository(Transport)

    def create(self, data):
        return self.repository.create(**data)

    def update(self, transport_id, data):
        transport = self.repository.get(transport_id)
        if transport:
            return self.repository.update(transport, **data)
        return None

    def get_all(self):
        transports = self.repository.all()
        serializer = TransportSerializer(transports, many=True)
        return serializer.data

    def get_by_id(self, transport_id):
        return self.repository.get(transport_id)

    def delete(self, transport_id):
        transport = self.repository.get(transport_id)
        if transport:
            self.repository.delete(transport)
            return True
        return False

    def get_transport_data(self):
        transport_data = Transport.objects.values('type').annotate(
            transports=Count('transportbooking__tour')
        ).order_by('-transports')

        df = pd.DataFrame(list(transport_data))
        return df
