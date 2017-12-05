from django.db import models

class User(models.Model):
    STATUS_CHOICES = (
        (0, 'Inactive'),
        (1, 'Active'),
    )
    ROLE_CHOICES = (
        (1, 'Admin'),
        (2, 'User'),
    )
    objects = models.Manager()

    username = models.CharField(max_length=150, null=False, blank=False, unique=True)
    password = models.CharField(max_length=254, null=False, blank=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    facebook = models.URLField()
    pin = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)

    def __str__(self):
        return '{} - {}'.format(self.username, self.email)

    def is_anonymous(self):
        return False