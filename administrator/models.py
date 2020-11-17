# Create your models here.
from django.contrib.sites.models import Site
from django.db import models


class MOSAIC_SITE(Site):
    MIN_BOOKING_HOURS = models.IntegerField(default=12)
