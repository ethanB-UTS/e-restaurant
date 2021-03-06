from django import forms
from django.conf import settings
from app.models.booking_model import Table, Booking
from django.forms import ValidationError
from datetime import datetime, timedelta
from django.utils import timezone

def get_available_tables(booking_start_date_time, booking_end_date_time, guests):
    l_bound_time = booking_start_date_time
    u_bound_time = booking_end_date_time

    tables_booked_ids = []
    # Exclude tables which start and end booking date includes requested initial booking date_time
    tables_booked = Booking.objects.filter(bookingStartDateTime__lt= l_bound_time, bookingEndDateTime__gt = l_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp
    for x in tables_booked:
        print(x)
    # Exclude tables which start and end booking date includes requested ending booking date_time
    tables_booked = Booking.objects.filter(bookingStartDateTime__lt = u_bound_time, bookingEndDateTime__gt = u_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp

    # Exclude tables which booking slots is inside requested booking slot
    tables_booked = Booking.objects.filter(bookingStartDateTime__gt = l_bound_time, bookingEndDateTime__lt = u_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp

    # Exclude tables which include requested booking slot
    tables_booked = Booking.objects.filter(bookingStartDateTime__lt = l_bound_time, bookingEndDateTime__gt = u_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp

    # Then I get a list of all the tables, of the needed size, available in that restaurant and
    # I exclude the previous list of unavailable tables. I order the list from the smaller table
    # to the bigger one and I return the first, smaller one, available.
    tables = Table.objects.filter(maxCapacity__gte=guests).exclude(id__in=tables_booked_ids)

    return tables


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class InitialBookingForm(forms.ModelForm):
    
    class Meta:
        model = Booking
        fields = [
            'guests',
            'bookingStartDateTime',
            'bookingEndDateTime',
        ]
        widgets = {
            'bookingStartDateTime' : DateTimeInput(),
            'bookingEndDateTime' : DateTimeInput(),
        }
        labels = {
            'guests' : 'Number of Guests:',
            'bookingStartDateTime' : 'Booking Start Time',
            'bookingEndDateTime' : 'Booking End Time',
        }
    
    def clean_guests(self):
        data = self.cleaned_data['guests']
        if data < 1:
                raise ValidationError("A booking must be for at least one person")
        return data
    def clean_user(self):
        data = self.cleaned_data['user']
        for obj in Booking.objects.all():
            if obj.user == data:
                raise ValidationError("You already have an active booking")
        return data
    def clean_bookingStartDateTime(self):
        data = self.cleaned_data['bookingStartDateTime']
        date = data.date
        now = timezone.now()
        if data < now:
            raise ValidationError("Bookings cannot be in the past")
        return data


    

class FinalBookingForm(forms.Form):  
    
    booking = Booking.objects.all().last()
    if(booking is None):
        table = forms.ModelChoiceField(queryset = Table.objects.all(), widget=forms.RadioSelect())
    else:
        table = forms.ModelChoiceField(queryset = get_available_tables(booking.bookingStartDateTime, booking.bookingEndDateTime, booking.guests), widget=forms.RadioSelect())

class editBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'guests',
            'table',
            'bookingStartDateTime',
            'bookingEndDateTime'
        ]
        widgets = {
            'bookingStartDateTime' : DateTimeInput(),
            'bookingEndDateTime' : DateTimeInput(),
        }
        labels = {
            'guests' : 'Number of Guests:',
            'bookingStartDateTime' : 'Booking Start Time',
            'bookingEndDateTime' : 'Booking End Time',
        }


