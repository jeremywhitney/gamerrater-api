from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    designer = models.CharField(max_length=255)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    estimated_time_to_play = models.IntegerField()
    age_recommendation = models.CharField(max_length=50)
    categories = models.ManyToManyField(
        "Category", through="GameCategory", related_name="games"
    )
    image_url = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    @property
    def average_rating(self):
        """Calculate the average rating for the game."""
        ratings = self.ratings.all()

        # Check if there are ratings
        if not ratings.exists():
            return 0

        # Sum all the ratings for the game
        total_rating = sum(rating.rating for rating in ratings)

        # Calculate the average rating
        average = total_rating / len(ratings)

        # Return the average rounded to one decimal place
        return round(average, 1)
