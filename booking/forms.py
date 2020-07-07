from crispy_forms.helper import FormHelper
from booking.models import Booking, Address
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Submit, Layout, Field


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time', 'address', 'customer', 'service', 'staff', 'key_no',
                  'job_reference', 'notes', 'private_notes']

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()


class AddressForm(ModelForm):
    lat = forms.CharField(widget=forms.HiddenInput(), required=True)
    long = forms.CharField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = Address
        fields = ['lat', 'long', 'street_name', 'details', 'suburb', 'state', 'postcode', 'country']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
