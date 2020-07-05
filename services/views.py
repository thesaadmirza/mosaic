from django.views.generic import ListView, DetailView, FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse
from services.models import Service, ServiceType
from services.forms import ServiceForm
from django.urls import reverse_lazy
import json


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


def get_service(request, type):
    if type and request.is_ajax():
        pk = type
        staff = Service.objects.filter(type__id=pk, add_on=False).values('id', 'name', 'price', 'time', 'description')
        data = list(staff)

        return HttpResponse(json.dumps({'service': data}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error': 'unable to find any Staff'}), content_type="application/json")
