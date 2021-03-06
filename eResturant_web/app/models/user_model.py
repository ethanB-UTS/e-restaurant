from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.db.models.deletion import CASCADE
# Create your models here.

# login/signup


class userProfile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    fName = models.CharField(max_length=50, name="First Name")
    lName = models.CharField(max_length=50, name="Last Name")
    isStaff = models.BooleanField(default=False)
    visits = models.IntegerField(default=0)
