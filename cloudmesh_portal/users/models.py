from django.db import models
from django.contrib.auth.models import User, Group
from django_countries.fields import CountryField


class PortalUser(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    address = models.CharField(max_length=100)
    additional_info = models.CharField(max_length=300)
    country = CountryField()
    citizen = CountryField()

    class Meta:
        verbose_name = 'Portal User'
        verbose_name_plural = 'Portal Users'

    @classmethod
    def create(cls, user, address, additional_info, country, citizen):
        portal_user = cls(user=user,address=address,
                          additional_info=additional_info,country=country,
                          citizen=citizen)
        return portal_user

    def __str__(self):
        return str(self.user)


class Settings(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)
    groups = models.ManyToManyField(Group)

    @classmethod
    def get_settings(cls, name, user, priority=User):
        user_settings = list(cls.objects.filter(name=name, users__in=[user]))
        group_settings = list(
            cls.objects.filter(name=name, groups__in=user.groups.all()))
        if user_settings and not group_settings:
            return user_settings
        elif group_settings and not user_settings:
            return group_settings
        else:
            return (group_settings, user_settings)[priority == User]
