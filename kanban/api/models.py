import jwt

from django.conf import settings
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=150)

    def generate_jwt(self):
        return jwt.encode(
            {"id": self.id}, settings.JWT_SECRET, algorithm="HS256"
        ).decode()
