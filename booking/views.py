from django.views.generic import ListView, DetailView, FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from booking.models import Booking, Address, BusinessHours
from services.models import Service, ServiceType
from booking.forms import BookingForm, AddressForm
from django.urls import reverse_lazy
from users.models import Customer, Staff
from administrator.models import MOSAIC_SITE
from django.shortcuts import render, HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime, timedelta
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
from django.utils.dateparse import parse_datetime
from utils.credentials import get_calendar_service
import datetime
import googlemaps
from users.models import Staff
import fsutil

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)


# Ends Here Google Calendar


@login_required
def calendar(request):
    events = Booking.objects.all()
    # Get Calendar Service from Utitls
    events_g = []
    try:
        if (request.user.social_auth.exists()):
            service = get_calendar_service(request)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = service.events().list(calendarId=request.user.email, timeMin=now,
                                                  maxResults=100, singleEvents=True,
                                                  orderBy='startTime').execute()

            events_g = events_result.get('items', [])
    except Exception as e:
        print(e)
    return render(request, 'admin/bookings/calendar.html', {'events': events, 'events_g': events_g})


# Create your views here.
class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    queryset = Booking.objects.all()
    template_name = 'admin/bookings/list.html'

    def get_queryset(self):
        return Booking.objects.reverse().all()


class BookingCreateView(LoginRequiredMixin, CreateView, FormView):
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


class BookingsUpdate(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy('booking:list')
    template_name = 'admin/bookings/update.html'

    def get_context_data(self, **kwargs):
        context = super(BookingsUpdate, self).get_context_data(**kwargs)
        context['AddressForm'] = AddressForm()
        context['main_services'] = Service.objects.filter(
            type=self.object.service.filter(add_on=False).first().type, add_on=False).all()
        context['staffs'] = Staff.objects.filter(
            customer=self.object.customer).all()
        context['total_minutes'] = (self.object.end_time - self.object.start_time).total_seconds() / 60.0
        context['service_types'] = ServiceType.objects.all()
        context['hours'] = BusinessHours.objects.all()
        context['services'] = Service.objects.filter(add_on=False)
        context['add_ons'] = Service.objects.filter(add_on=True)
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        form.instance.user = self.request.user
        return super(BookingsUpdate, self).form_valid(form)


class BookingDelete(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'admin/bookings/delete.html'
    success_url = reverse_lazy('booking:list')


def booking_events_json(request):
    bookings = Booking.objects.values('name', 'start_time', 'end_time')
    data = list(bookings)
    return HttpResponse(json.dumps(data), content_type="application/json")


def booking_json_modal(request, pk):
    booking = Booking.objects.filter(id=pk).first()
    if booking:
        services = booking.service.all()
        services_all = []
        for service in services:
            service_obj = {
                'type': service.type.name,
                'name': service.name,
                'price': service.price,
                'time': service.time,
            }
            services_all.append(service_obj)
        data = {
            'id': booking.id,
            'address': booking.address.full_addreess,
            'lat': booking.address.lat,
            'long': booking.address.long,
            'start_time': booking.start_time,
            'services': services_all,
            'end_time': booking.end_time,
            'customer': booking.customer.company_name,
            'staff': booking.staff.name,
            'url': reverse('booking:update', kwargs={'pk': booking.id}),

        }
        return JsonResponse({'message': 'success', 'data': data}, status=200)
    else:
        return JsonResponse({'message': 'Not Found'}, status=400)


def update_booking(request, pk):
    booking = Booking.objects.filter(id=pk).first()
    selected_customer = request.POST.get('customer', booking.customer.id)
    customer = Customer.objects.filter(id=selected_customer).first()
    address = Address.objects.filter(id=booking.address.pk).first()
    address_updated = Address.objects.filter(id=booking.address.pk).update(
        street_name=request.POST.get('street_name', address.street_name),
        country=request.POST.get('country', address.country),
        suburb=request.POST.get('suburb', address.suburb), lat=request.POST.get('lat', address.lat),
        long=request.POST.get('long', address.long),
        customer=customer, details=request.POST.get('details', address.details),
        state=request.POST.get('state', address.state),
        postcode=request.POST.get('postcode', address.postcode),
        full_addreess=request.POST.get('address_det', address.full_addreess))
    booking.customer = customer
    booking.staff = Staff.objects.get(id=request.POST.get('staff', booking.staff.id))
    start_time = request.POST.get('start_time', False)
    if start_time:
        booking.start_time = parse_datetime(start_time)
    else:
        start_time = booking.start_time
    total_minutes = request.POST['total_minutes']
    booking.end_time = booking.start_time + datetime.timedelta(minutes=int(total_minutes))
    booking.key_no = request.POST.get('key_no', booking.key_no)
    booking.job_reference = request.POST.get('job_reference', booking.job_reference)
    booking.notes = request.POST.get('notes', booking.notes)
    booking.private_notes = request.POST.get('private_notes', booking.private_notes)
    booking.save()

    service = Service.objects.get(id=request.POST.get('services'))
    if service:
        booking.service.clear()
        booking.service.add(service)
        if (request.POST.getlist('add_on')):
            for add in request.POST.getlist('add_on'):
                service = Service.objects.get(id=add)
                booking.service.add(service)
        booking.save()
    return redirect('/booking/edit/' + str(booking.id) + '/')


@login_required
def store_booking(request):
    address = AddressForm(request.POST)
    addr = None
    start_time = parse_datetime(request.POST['start_time'])
    booked = Booking.objects.filter(start_time=start_time).count()
    if booked:
        print("Booking Already Exist at this slot")  # todo error message display
        return redirect('/booking')
    if (address.is_valid()):
        customer = Customer.objects.get(id=request.POST['customer'])
        addr = Address.objects.create(street_name=request.POST['street_name'], country=request.POST['country'],
                                      suburb=request.POST['suburb'], lat=request.POST['lat'], long=request.POST['long'],
                                      customer=customer, details=request.POST['details'], state=request.POST['state'],
                                      postcode=request.POST['postcode'], full_addreess=request.POST['address_det'])
    else:
        customer = Customer.objects.get(id=request.POST['customer'])
        addr = Address.objects.create(street_name=request.POST['street_name'], country=request.POST['country'],
                                      suburb=request.POST['suburb'], lat=request.POST['lat'], long=request.POST['long'],
                                      customer=customer, details=request.POST['details'], state=request.POST['state'],
                                      postcode=request.POST['postcode'], full_addreess=request.POST['address_det'])

    customer = Customer.objects.get(id=request.POST['customer'])
    staff = Staff.objects.get(id=request.POST['staff'])
    service = Service.objects.get(id=request.POST['services'])
    addres = Address.objects.get(id=addr.id)
    updated_data = request.POST.copy()

    total_minutes = request.POST['total_minutes']
    end_time = start_time + datetime.timedelta(minutes=int(total_minutes))
    updated_data.update({'start_time': start_time,
                         'end_time': end_time, 'address': addres,
                         'customer': customer, 'staff': staff, 'key_no': request.POST['key_no'],
                         'job_reference': request.POST['job_reference'], 'notes': request.POST['notes'],
                         'private_notes': request.POST['private_notes']})

    booking = BookingForm(data=updated_data)

    if booking.is_valid():

        savedB = booking.save()
        savedB.end_time = savedB.start_time + timedelta(minutes=service.time)
        service = Service.objects.get(id=request.POST['services'])
        savedB.service.add(service)
        if (request.POST.getlist('add_on')):
            for add in request.POST.getlist('add_on'):
                service = Service.objects.get(id=add)
                savedB.end_time = savedB.end_time + timedelta(minutes=service.time)
                savedB.service.add(service)

        savedB.save()
        description = 'Address : ' + savedB.address.full_addreess + '<br>' + 'Customer : ' + customer.company_name + '<br>' + 'Staff : ' + staff.name
        try:
            foldername = str(savedB.id) + ' - ' + savedB.address.full_addreess
            dir_project = settings.PROJECT_ROOT + '/' + foldername
            savedB.project_folder = foldername
            savedB.save()
            not_exist = fsutil.assert_not_dir(dir_project)
            if not_exist:
                fsutil.delete_dir(dir_project)
            else:
                fsutil.create_dir(dir_project, overwrite=False)
        except Exception as e:
            print(e)

        try:
            service = get_calendar_service(request)
            event = service.events().insert(calendarId=request.user.email
                                            , body={
                    'summary': savedB.address.full_addreess,
                    'location': savedB.address.full_addreess,
                    'description': description,
                    'status': 'confirmed',
                    'notes': savedB.notes,
                    'start': {'dateTime': savedB.start_time.isoformat()},
                    'end': {'dateTime': savedB.end_time.isoformat()},
                    'sendNotifications ': True,
                    'attendees': [
                        {'email': customer.user.email},
                        {'email': staff.user.email},
                    ],
                }).execute()
        except Exception as e:
            print(e)

    else:

        print("error", booking)

    return redirect('/booking')


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if x >= start and x <= end:
        return True
    else:
        return False


def createSlots(startTime, endTime, date, slot_duration):
    slots = []
    t = datetime.datetime.combine(date, startTime)
    endTime = datetime.datetime.combine(date, endTime)
    slots.append(t)
    while t <= endTime:
        t = t + datetime.timedelta(minutes=15)
        if t <= endTime and t + datetime.timedelta(minutes=slot_duration) <= endTime:
            slots.append(t)
    return slots


def getSlots(hours, date, slot_duration, lat, lang):
    slots = []
    for hour in hours:
        createdSlots = createSlots(hour.from_hour, hour.to_hour, date, slot_duration)
        slots = slots + createdSlots
    slots = list(dict.fromkeys(slots))
    slots.sort(reverse=False)
    bookings = Booking.objects.filter(start_time__date=date).values('start_time', 'end_time', 'address__lat',
                                                                    'address__long').all()
    destination = (lat, lang)
    for book in bookings:
        origin = (book['address__lat'], book['address__long'])
        try:
            gresult = gmaps.distance_matrix(origin, destination, mode='driving')
            result_time = gresult["rows"][0]["elements"][0]["duration"]["value"]
            result_time = result_time / 60
            result_time = int(round(result_time))
        except Exception as e:
            result_time = 0
            print(e)

        start_time = book['start_time'] - datetime.timedelta(
            minutes=int(result_time))
        end_time = book['end_time'] + datetime.timedelta(
            minutes=int(result_time))
        result = [i for i in slots if (i >= start_time and i <= end_time) or (i + datetime.timedelta(
            minutes=slot_duration) >= start_time and i <= start_time)]
        if result:
            slots = list(set(slots) - set(result))

    slots.sort(reverse=False)
    return slots


def timeCalendar(request):
    import datetime
    date = datetime.date.today()
    next = request.GET.get('next', False)
    previous = request.GET.get('previous', False)
    slot_duration = 45
    if next or previous:
        if next:

            start_week = datetime.datetime.strptime(next, "%Y-%m-%d").date()
        else:

            start_week = datetime.datetime.strptime(previous, "%Y-%m-%d").date()
    else:
        start_week = date - datetime.timedelta(date.weekday())
    start_week = date - datetime.timedelta(date.weekday())
    weekdays = date.weekday()
    days = []
    days.append(start_week)
    previous = start_week - datetime.timedelta(6)
    next = start_week + datetime.timedelta(7)
    for i in range(1, 7):
        days.append(start_week + datetime.timedelta(i))
    newdays = []
    for index, value in enumerate(days):
        data = {}
        data['day'] = value
        weekday = value.weekday() + 1
        if date <= value:

            hours = BusinessHours.objects.filter(weekday=weekday).all()
            data['slots'] = getSlots(hours, value, slot_duration)
        else:
            data['slots'] = []
        newdays.append(data)

    return render(request, 'admin/bookings/timeCalendar.html',
                  context={'days': newdays, 'today': date, 'previous': previous, 'next': next})


def timeCalendar_json(request):
    import datetime
    date = datetime.date.today()
    next = request.GET.get('next', False)
    previous = request.GET.get('previous', False)
    slot_duration = int(request.GET.get('slot_duration', 15))
    lat = request.GET.get('lat', False)
    lang = request.GET.get('lang', False)
    if next or previous:
        if next:

            start_week = datetime.datetime.strptime(next, "%Y-%m-%d").date()
        else:

            start_week = datetime.datetime.strptime(previous, "%Y-%m-%d").date()
    else:
        start_week = date - datetime.timedelta(date.weekday())
    weekdays = date.weekday()
    days = []
    days.append(start_week)
    previous = start_week - datetime.timedelta(6)
    next = start_week + datetime.timedelta(7)
    for i in range(1, 7):
        days.append(start_week + datetime.timedelta(i))
    newdays = []
    MIN_BOOKING_HOURS = MOSAIC_SITE.objects.first()
    if MIN_BOOKING_HOURS:
        MIN_BOOKING_HOURS = MIN_BOOKING_HOURS.MIN_BOOKING_HOURS
    else:
        MIN_BOOKING_HOURS = settings.MIN_BOOKING_HOURS
    for index, value in enumerate(days):
        data = {}
        data['day'] = value
        weekday = value.weekday() + 1
        if date + datetime.timedelta(hours=MIN_BOOKING_HOURS) <= value:
            hours = BusinessHours.objects.filter(weekday=weekday).all()
            data['slots'] = getSlots(hours, value, slot_duration, lat, lang)
        else:
            data['slots'] = []
        newdays.append(data)

    converted_string = render_to_string('admin/bookings/render_calendar.html',
                                        {'days': newdays, 'today': date, 'previous': previous, 'next': next})
    return HttpResponse(converted_string)
