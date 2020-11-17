from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from users.models import Customer, Staff
from services.models import Service

WEEKDAYS = [
    (1, _("Monday")),
    (2, _("Tuesday")),
    (3, _("Wednesday")),
    (4, _("Thursday")),
    (5, _("Friday")),
    (6, _("Saturday")),
    (7, _("Sunday")),
]


class BusinessHours(models.Model):
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'from_hour', 'to_hour')

    def __str__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                                 self.from_hour, self.to_hour)


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses")
    lat = models.CharField(_("Latitude"), max_length=30)
    long = models.CharField(_("Longitude"), max_length=30)
    full_addreess = models.CharField(_("Full Address"), max_length=250)
    street_name = models.CharField(_("Street Number and Name"), max_length=100, blank=True, null=True)
    details = models.CharField(_("Details"), max_length=100, blank=True, null=True)
    suburb = models.CharField(_("Suburb"), max_length=100, blank=True, null=True)
    state = models.CharField(_("State"), max_length=100, blank=True, null=True)
    postcode = models.CharField(_("Postcode"), max_length=50, blank=True, null=True)
    country = models.CharField(_("Country"), max_length=50)

    def __str__(self):
        return str(self.full_addreess)


# Create your models here.
class Booking(models.Model):
    NO_ACESSS = "NO"
    OWNER = "OW"
    KEYS = "KE"
    STAFF = "ST"
    SITE = "SI"
    ARRANGEMENTS_CHOICES = (
        (NO_ACESSS, _("No Private Access Required")),
        (OWNER, _("Owner or Tenant will be at home")),
        (KEYS, _("Pick up keys from office")),
        (STAFF, _("Client staff member will attend")),
        (SITE, _("Keys available on site in lock box"))

    )
    start_time = models.DateTimeField(_("Start Time"))
    end_time = models.DateTimeField(_("End Time"))
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="bookings_customer")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bookings_address")
    service = models.ManyToManyField(Service, related_name="bookings", blank=True, null=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="bookings_services", blank=True, null=True)
    # access_arrangments = models.CharField(_("Access Arrangements"), max_length=10, choices=ARRANGEMENTS_CHOICES)
    key_no = models.CharField(_("Key Number"), max_length=100, blank=True, null=True)
    job_reference = models.CharField(_("Client Job reference"), max_length=100, blank=True, null=True)
    notes = models.TextField(_("Notes"), blank=True, null=True)
    private_notes = models.TextField(_("Private Notes"), null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('booking:view', kwargs={'pk': self.pk})

    def services_types_names(self):
        return self.service.values_list('type__name')

    def save(self, *args, **kwargs):
        self.start_time = self.start_time.replace(tzinfo=None)
        self.end_time = self.end_time.replace(tzinfo=None)
        super(Booking, self).save(*args, **kwargs)
