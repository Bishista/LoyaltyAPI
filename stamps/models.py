from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime

class Stamp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now)


    def __str__(self):
        return f"{self.user.username} - Stamp on {self.created_at}"
