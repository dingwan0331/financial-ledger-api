from django.db import models

from apps.util.models   import TimeStampModel
from apps.auth.managers import UserManager
class User(TimeStampModel):
    email    = models.CharField(max_length=200, unique=True)
    password = models.BinaryField(max_length=60)

    objects  = UserManager()

    class Meta():
        db_table = 'users'