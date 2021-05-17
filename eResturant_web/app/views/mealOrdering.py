from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from app.models import MealOrder, Booking, Menu
from django import forms
from app.forms.meal_forms import MealOrderForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def meal_order_view(request):
    if Booking.objects.filter(user = request.user).count() == 0:
        return redirect('/create')

    current_booking = Booking.objects.get(user = request.user)
    MealOrders = MealOrder.objects.filter(booking = current_booking)

    list = []
    for orders in MealOrders:
        list.append(orders.order.name + "(" + orders.order.category + ") : $" + str(orders.order.price))

    return render(request, 'app/meal_order.html', {'list' : list})
@login_required
def edit_order_view(request):
    template = 'app/meal_order_edit.html'
    context = {}
    current_user = request.user

    if Booking.objects.filter(user = current_user):
        current_booking = Booking.objects.get(user = request.user)
    else:
        return redirect('/create')

    MealOrders = MealOrder.objects.filter(booking = current_booking)
    MealOrders.delete()

    return render(request, template, context)

@login_required
def make_order_view(request):   

    form = MealOrderForm(request.POST or None)
    current_user = request.user
    
    if Booking.objects.filter(user = current_user).count() == 0:
            return redirect('/create')

    this_booking = Booking.objects.filter(user = current_user)
    if form.is_valid():
        f = form.save(commit=False)
        f.booking = this_booking.first()
        f.save()
    
    context = {'form': form}

    return render(request, 'app/order.html', context)
