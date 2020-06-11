from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Staff, Customer, User
from utils.strings import get_random_alphaNumeric_string
from users.forms import StaffForm, StaffFormE
from django.urls import reverse_lazy

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.utils import ErrorList


# Create your views here.
class StaffListView(ListView, LoginRequiredMixin):
    model = Staff
    queryset = Staff.objects.all()
    template_name = 'admin/staff/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StaffListView, self).get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(id=self.kwargs.get('customer'))
        return context

    def get_queryset(self):
        return Staff.objects.filter(customer_id__exact=self.kwargs.get('customer'))


class StaffCreateView(CreateView, LoginRequiredMixin):
    model = Staff
    form_class = StaffForm
    template_name = 'admin/staff/add.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StaffCreateView, self).get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(id=self.kwargs.get('customer'))
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if email:
            exist = User.objects.filter(email=email)
            if (exist):
                form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
                    _('Email Already Exist')
                ])
                return self.form_invalid(form)
            else:
                passw = get_random_alphaNumeric_string(8)
                # todo send email to customer with passsword using SMTP
                user = User.objects.create(email=email, password=passw, type='C', username=passw)

        else:
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
                _('Email Field is Invalid')
            ])
            return self.form_invalid(form)
        form.instance.customer = Customer.objects.get(id=self.kwargs.get('customer'))
        form.instance.user = user
        return super().form_valid(form)


class StaffUpdate(UpdateView):
    model = Staff
    form_class = StaffFormE
    template_name = 'admin/staff/update.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StaffUpdate, self).get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(id=self.kwargs.get('customer'))
        return context

    def get_success_url(self):
        return reverse_lazy('staff:index', kwargs={'customer': self.kwargs.get('customer')})


class StaffView(DetailView):
    model = Staff
    template_name = 'admin/staff/view.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StaffView, self).get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(id=self.kwargs.get('customer'))
        return context


class StaffDelete(DeleteView):
    model = Staff
    template_name = 'admin/staff/delete.html'

    def get_success_url(self):
        return reverse_lazy('staff:index', kwargs={'customer': self.kwargs.get('customer')})