from django.db import models

from apps.util.models import TimeStampModel

class Transaction(TimeStampModel):
    deposit          = models.IntegerField()
    # Index처리를위해 IntegerField 사용
    transaction_date = models.IntegerField()
    title            = models.CharField(max_length = 20)
    description      = models.CharField(max_length = 100)
    user             = models.ForeignKey('auth.User', on_delete = models.CASCADE)

    class Meta():
        db_table = 'transactions'