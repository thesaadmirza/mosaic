from django.contrib import admin
from users.models import User, Customer, Staff
from allauth.socialaccount.models import SocialToken

# Register your models here.

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Staff)

