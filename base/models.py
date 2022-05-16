from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    competitor_name = models.CharField(default='', max_length=200)
    event_name = models.CharField(default='', max_length=200)
    division = models.CharField(default='', max_length=200)
    ring = models.CharField(max_length=10, null=True, blank=True)
    competitors = models.TextField(null=True, blank=True)
    results = models.CharField(max_length=200, null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.competitor_name

    class Meta:
        order_with_respect_to = 'user'
