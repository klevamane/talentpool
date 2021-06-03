from django.db import models


class TimeStampMixin(models.Model):
    """A utility class

    indicating when an object is created and updated.
    """
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class AddressMixin(models.Model):
    """Address details

     This class can only be inherited and cannot
     create a database table
     """
    address1 = models.CharField(max_length=30, blank=True, null=True)
    area = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    postal_code = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        abstract = True
