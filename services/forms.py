from crispy_forms.helper import FormHelper
from services.models import Service
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Submit, Layout, Field


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'time']

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
