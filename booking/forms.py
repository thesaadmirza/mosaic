from crispy_forms.helper import FormHelper
from booking.models import Booking
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Submit, Layout, Field


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time', 'address', 'customer', 'service', 'staff', 'access_arrangments', 'key_no',
                  'job_reference', 'notes', 'private_notes']

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
