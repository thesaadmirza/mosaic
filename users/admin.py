from django.contrib import admin
from users.models import User, Customer, Staff

# Register your models here.

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Staff)
