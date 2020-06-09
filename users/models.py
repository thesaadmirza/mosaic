from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    STAFF = "S"
    CUSTOMER = "C"
    USER_TYPES = (
        (STAFF, _("Staff")),
        (CUSTOMER, _("Customer")),
    )
    type = models.CharField(max_length=10, choices=USER_TYPES)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
