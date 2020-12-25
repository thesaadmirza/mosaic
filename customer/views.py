from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User, Customer
from users.forms import UserForm, CustomerForm, CustomerFormE
from django.forms.utils import ErrorList
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.urls import reverse_lazy
from utils.strings import get_random_alphaNumeric_string



# Create your views here.


# Create your views here.
class CustomersListView(LoginRequiredMixin, ListView):
    model = Customer
    queryset = Customer.objects.all()
    template_name = 'admin/customers/list.html'





class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'admin/customers/add.html'

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

        form.instance.user = user
        return super().form_valid(form)


class CustomerView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'admin/customers/view.html'


class CustomersUpdate(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerFormE
    success_url = reverse_lazy('customer:index')
    template_name = 'admin/customers/update.html'

class CustomerDelete(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'admin/customers/delete.html'
    success_url = reverse_lazy('customer:list')
