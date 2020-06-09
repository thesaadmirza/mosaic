from django.views.generic import ListView, DetailView, FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from services.models import Service
from services.forms import ServiceForm
from django.urls import reverse_lazy


# Create your views here.
class ServicesListView(ListView, LoginRequiredMixin):
    model = Service
    queryset = Service.objects.all()
    template_name = 'admin/services/list.html'


class ServicesCreateView(CreateView, FormView):
    model = Service
    form_class = ServiceForm
    template_name = 'admin/services/add.html'


class ServicesUpdate(UpdateView):
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy('services:list')
    template_name = 'admin/services/update.html'


class ServiceDelete(DeleteView):
    model = Service
    template_name = 'admin/services/delete.html'
    success_url = reverse_lazy('services:list')


class ServiceView(DetailView):
    model = Service
    template_name = 'admin/services/view.html'
