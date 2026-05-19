from django.contrib.auth.models import User
from django.db import models

from images.models import OSImage


class Deployment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(OSImage, on_delete=models.CASCADE)
    container_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.container_id
