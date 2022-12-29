from django.db import models

from datetime import datetime

def timestamp_now():
    return datetime.now().timestamp()    

class TimeStampModel(models.Model):
    created_at = models.FloatField(default = timestamp_now)
    updated_at = models.FloatField(default = timestamp_now)
    
    class Meta:
        abstract = True