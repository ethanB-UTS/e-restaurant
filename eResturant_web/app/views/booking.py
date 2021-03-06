from django.shortcuts import render
from django.http import HttpResponse
from app.models.booking_model import Booking, Table
from app.models.user_model import userProfile
from app.forms.booking_forms import InitialBookingForm, editBookingForm, FinalBookingForm
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import redirect
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def bookings_view(request):
    try:
        booking = Booking.objects.get(user=request.user)
    except Booking.DoesNotExist:
        booking = None
    user = request.user
    my_context = {
        'booking': booking,
        'user': user
    }
    return render(request, 'app/bookings.html', my_context)


@login_required
def booking_create_view(request):

    initial_form = InitialBookingForm(request.POST or None)
    current_user = request.user
    if initial_form.is_valid():
        if Booking.objects.filter(user=current_user).count() == 0:
            f = initial_form.save(commit=False)
            f.user = current_user
            visits = userProfile.objects.get(user_id=f.user)
            userC = userProfile.objects.filter(
                user_id=f.user).update(visits=visits.visits + 1)
            f.save()
            return redirect("bookings/create/table")
        else:
            return redirect("bookings/existing")

    return render(request, 'app/bookings_create.html', {'initial_form': initial_form})


@login_required
def booking_existing_view(request):
    return render(request, 'app/bookings_existing.html')


@login_required
def booking_create_table_view(request):
    table_form = FinalBookingForm(request.POST or None)
    if table_form.is_valid():
        booking = Booking.objects.all().last()
        booking.table = table_form.cleaned_data.get('table')
        booking.save()

        return redirect("bookings")
    return render(request, 'app/bookings_create_table.html', {'table_form': table_form})


@login_required
def booking_edit_view(request, *args, **kwargs):
    form = editBookingForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = BookingForm()
    context = {
        'form': form
    }
    return render(request, 'app/bookings_edit.html', context)


@login_required
def booking_delete_edit_view(request, *args, **kwargs):
    try:
        booking = Booking.objects.get(user=request.user)
        date = booking.bookingStartDateTime
        if date - timezone.now() > timedelta(days=1):
            booking.delete()
            return redirect("bookings/create")
        else:
            return redirect("bookings/edit/fail")
    except Booking.DoesNotExist:
        return redirect("bookings/create")


@login_required
def booking_delete_view(request):
    try:
        booking = Booking.objects.get(user=request.user)
        booking.delete()
        return redirect("bookings")
    except Booking.DoesNotExist:
        return redirect("bookings")


@login_required
def booking_edit_fail_view(request):
    return render(request, 'app/bookings_edit_fail.html')
