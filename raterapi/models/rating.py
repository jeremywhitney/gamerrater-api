from django.db import models
from django.contrib.auth.models import User


class Rating(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        if not (1 <= self.rating <= 10):
            raise ValueError("Rating must be between 1 and 10.")
        super().save(*args, **kwargs)
