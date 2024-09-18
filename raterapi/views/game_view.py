from rest_framework import serializers, viewsets
from raterapi.models import Game, Category
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


class GameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    created_by = GameUserSerializer(read_only=True)
    categories = GameCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = (
            "id",
            "title",
            "description",
            "designer",
            "year_released",
            "number_of_players",
            "estimated_time_to_play",
            "age_recommendation",
            "created_by",
            "categories",
        )


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all().order_by("title")
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated

    def perform_create(self, serializer):
        # Save the game object first
        game = serializer.save(created_by=self.request.user)
        # Manually assign categories after the game has been created
        categories = self.request.data.get("categories")
        if categories:
            game.categories.set(categories)
            game.save()
