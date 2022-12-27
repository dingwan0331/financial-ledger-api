from django.db import models

from ..util.models import TimeStampModel

class User(TimeStampModel):
    email    = models.CharField(max_length=200, unique=True)
    password = models.BinaryField(max_length=60)

    class Meta():
        db_table = 'users'