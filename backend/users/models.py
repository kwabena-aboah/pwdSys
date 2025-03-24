from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	ROLE_CHOICES = [
		('admin', 'Administrator'),
		('social_worker', 'Social Worker'),
		('medical_officer', 'Medical Officer'),
	]
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='social_worker')
