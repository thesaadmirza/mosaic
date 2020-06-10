from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User, Customer
from users.forms import UserForm, CustomerForm
from django.urls import reverse_lazy


@login_required
def index(request):
    return render(request, 'admin/dashboard.html', {})


# Create your views here.
class CustomersListView(ListView, LoginRequiredMixin):
    model = Customer
    queryset = Customer.objects.all()
    template_name = 'admin/customers/list.html'
