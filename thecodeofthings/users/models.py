from django.contrib.auth import models as auth_models
from django.db import models


class User(auth_models.AbstractUser):
    resource = models.URLField(blank=True)
    twitter_username = models.CharField(max_length=15, blank=True)
