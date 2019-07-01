from django.db import models
from the_platform import settings

REASONABLE_LENGTH = settings.REASONABLE_CONSTANTS['TEXT_FIELD']


class Tester(models.Model):
    '''
    Registered user on the platform.
    '''
    testerId = models.IntegerField(primary_key=True)
    firstName = models.CharField("first name", max_length=REASONABLE_LENGTH)
    lastName = models.CharField("last name", max_length=REASONABLE_LENGTH)
    country = models.CharField(
        "country ID", max_length=2)
    # "2013-08-04 23:57:38" agrees with default Django one
    lastLogin = models.DateTimeField("last login", auto_now=True)


class Device(models.Model):
    '''
    Devices' ids and names.
    '''
    deviceId = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=REASONABLE_LENGTH)


class TesterDevice(models.Model):
    '''
    Data on what device a user interacted with.
    '''
    testerId = models.ForeignKey(Tester, on_delete=models.CASCADE)
    deviceId = models.ForeignKey(Device, on_delete=models.CASCADE)


class Bug(models.Model):
    '''
    Bugs reported by a user on a device.
    '''
    bugId = models.IntegerField(primary_key=True)
    deviceId = models.ForeignKey(Device, on_delete=models.CASCADE)
    testerId = models.ForeignKey(Tester, on_delete=models.CASCADE)
