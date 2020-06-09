from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


# Create your models here.
class Service(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    description = models.CharField(_("Description"), max_length=250)
    price = models.FloatField(_("Price"))
    time = models.IntegerField(_("Minutes"))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('services:view', kwargs={'pk': self.pk})
