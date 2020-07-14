from django.views.generic import ListView, DetailView, FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from booking.models import Booking, Address, BusinessHours
from services.models import Service, ServiceType
from booking.forms import BookingForm, AddressForm
from django.urls import reverse_lazy
from users.models import Customer, Staff
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime, timedelta
from django.utils import dateparse
from django.shortcuts import redirect


@login_required
def calendar(request):
    events = Booking.objects.all()
    return render(request, 'admin/bookings/calendar.html', {'events': events})


# Create your views here.
class BookingListView(ListView, LoginRequiredMixin):
    model = Booking
    queryset = Booking.objects.all()
    template_name = 'admin/bookings/list.html'

    def get_queryset(self):
        return Booking.objects.reverse().all()


class BookingCreateView(CreateView, FormView):
    model = Booking
    form_class = BookingForm
    template_name = 'admin/bookings/add.html'

    def get_context_data(self, **kwargs):
        context = super(BookingCreateView, self).get_context_data(**kwargs)
        context['AddressForm'] = AddressForm()
        context['service_types'] = ServiceType.objects.all()
        context['hours'] = BusinessHours.objects.all()
        context['services'] = Service.objects.filter(add_on=False)
        context['add_ons'] = Service.objects.filter(add_on=True)
        return context


class BookingsUpdate(UpdateView):
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy('booking:list')
    template_name = 'admin/bookings/update.html'


class BookingDelete(DeleteView):
    model = Booking
    template_name = 'admin/bookings/delete.html'
    success_url = reverse_lazy('booking:list')


class BookingView(DetailView):
    model = Booking
    template_name = 'admin/bookings/view.html'


def booking_events_json(request):
    bookings = Booking.objects.values('name', 'start_time', 'end_time')
    data = list(bookings)
    return HttpResponse(json.dumps(data), content_type="application/json")


def store_booking(request):
    address = AddressForm(request.POST)
    addr = None
    if (address.is_valid()):
        customer = Customer.objects.get(id=request.POST['customer'])
        addr = Address.objects.create(street_name=request.POST['street_name'], country=request.POST['country'],
                                      suburb=request.POST['suburb'], lat=request.POST['lat'], long=request.POST['long'],
                                      customer=customer, details=request.POST['details'], state=request.POST['state'],
                                      postcode=request.POST['postcode'])
    else:
        customer = Customer.objects.get(id=request.POST['customer'])
        addr = Address.objects.create(street_name=request.POST['street_name'], country=request.POST['country'],
                                      suburb=request.POST['suburb'], lat=request.POST['lat'], long=request.POST['long'],
                                      customer=customer, details=request.POST['details'], state=request.POST['state'],
                                      postcode=request.POST['postcode'])

    customer = Customer.objects.get(id=request.POST['customer'])
    staff = Staff.objects.get(id=request.POST['staff'])
    service = Service.objects.get(id=request.POST['services'])
    addres = Address.objects.get(id=addr.id)
    updated_data = request.POST.copy()
    updated_data.update({'start_time': dateparse.parse_datetime(request.POST['start_time']),
                         'end_time': dateparse.parse_datetime(request.POST['end_time']), 'address': addres,
                         'customer': customer, 'staff': staff, 'key_no': request.POST['key_no'],
                         'job_reference': request.POST['job_reference'], 'notes': request.POST['notes'],
                         'private_notes': request.POST['private_notes']})

    booking = BookingForm(data=updated_data)

    if booking.is_valid():

        savedB = booking.save()
        service = Service.objects.get(id=request.POST['services'])
        savedB.service.add(service)
        if (request.POST.getlist('add_on')):
            for add in request.POST.getlist('add_on'):
                service = Service.objects.get(id=add)
                savedB.service.add(service)

        savedB.save()


    else:

        print("error", booking)

    return redirect('/booking')
