from django import forms
from api.models import Tour

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = [
            'name', 'destination_city', 'destination_country', 'description',
            'start_date', 'end_date', 'price', 'tourist_count',
            'image_url', 'hotel_booking', 'transport_booking'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
