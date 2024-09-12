from django.db import models
from django.contrib.auth.models import User


class Picture(models.Model):
    image = models.ImageField(upload_to='pictures/')
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
