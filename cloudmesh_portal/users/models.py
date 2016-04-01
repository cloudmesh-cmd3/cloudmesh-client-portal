from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class PortalUser(models.Model):
    user = models.ForeignKey(User)
    address = models.CharField(max_length=100)
    additional_info = models.CharField(max_length=300)
    country = CountryField()
    citizen = CountryField()

    class Meta:
        verbose_name = 'Portal User'
        verbose_name_plural = 'Portal Users'

    def __str__(self):
        return self.user
