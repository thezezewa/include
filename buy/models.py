from django.db import models
from django.contrib.auth.models import AbstractUser

"""
유저별 기본 cash는 10,000원을 제공하는 것으로 합니다.
"""
class User(AbstractUser):
    cash = models.IntegerField(default=10000)
