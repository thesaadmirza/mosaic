from django.views.generic import ListView, DetailView, FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from booking.models import Booking
from services.forms import ServiceForm
from booking.forms import BookingForm
from django.urls import reverse_lazy


# Create your views here.
class BookingListView(ListView, LoginRequiredMixin):
    model = Booking
    queryset = Booking.objects.all()
    template_name = 'admin/bookings/list.html'


class BookingCreateView(CreateView, FormView):
    model = Booking
    form_class = BookingForm
    template_name = 'admin/bookings/add.html'


class BookingsUpdate(UpdateView):
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy('booking:list')
    template_name = 'admin/bookings/update.html'


class BookingDelete(DeleteView):
    model = Booking
    template_name = 'admin/bookings/delete.html'
    success_url = reverse_lazy('bookings:list')


class BookingView(DetailView):
    model = Booking
    template_name = 'admin/bookings/view.html'
