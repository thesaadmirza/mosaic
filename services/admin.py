from django.contrib import admin
from services.models import Service, ServiceType

# Register your models here.

admin.site.register(ServiceType)
admin.site.register(Service)
