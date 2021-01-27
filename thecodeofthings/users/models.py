from django.contrib.auth import models as auth_models
from django.db import models


class User(auth_models.AbstractUser):
    resource = models.URLField(blank=True)
