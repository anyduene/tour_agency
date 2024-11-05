from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    star_rating = models.IntegerField()
    mobile_phone = models.IntegerField()
    site = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'Hotel'

    def __str__(self):
        return self.name

class HotelBooking(models.Model):
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'HotelBooking'

    def __str__(self):
        return f"Booking for {self.hotel.name} from {self.check_in_date} to {self.check_out_date}"


class Transport(models.Model):
    type = models.CharField(max_length=255)

    class Meta:
        db_table = 'Transport'

    def __str__(self):
        return self.type


class TransportBooking(models.Model):
    arrival_date = models.DateField()
    place = models.CharField(max_length=255, null=True, blank=True)
    departure_point = models.CharField(max_length=255)
    departure_date = models.DateField()
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)

    class Meta:
        db_table = 'TransportBooking'

    def __str__(self):
        return f"Transport Booking {self.transport.type} from {self.departure_point} on {self.departure_date}"


class Tour(models.Model):
    destination_city = models.CharField(max_length=255)
    description = models.TextField()
    name = models.CharField(max_length=255)
    destination_country = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tourist_count = models.IntegerField()
    image_url = models.URLField(null=True, blank=True)
    hotel_booking = models.ForeignKey(HotelBooking, null=True, blank=True, on_delete=models.SET_NULL)
    transport_booking = models.ForeignKey(TransportBooking, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'Tour'

    def __str__(self):
        return f"Tour: {self.name} to {self.destination_city}, {self.destination_country}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
    ]
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        db_table = 'Booking'

    def __str__(self):
        return f"Booking for {self.client} on {self.tour.name} - {self.status}"