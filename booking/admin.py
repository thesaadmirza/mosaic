from django.contrib import admin
from booking.models import Address, Booking, BusinessHours

# Register your models here.
admin.site.register(Address)
admin.site.register(Booking)
admin.site.register(BusinessHours)
