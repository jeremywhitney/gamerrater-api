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
    created_by = GameUserSerializer(read_only=True)
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        write_only=True,  # This allows you to submit category IDs for updates
    )
    categories_detail = GameCategorySerializer(
        source="categories",
        many=True,
        read_only=True,  # This returns the detailed category information
    )
    average_rating = serializers.ReadOnlyField()
    image_url = serializers.URLField(required=False)

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
            "categories",  # For updates
            "categories_detail",  # For reading detailed category info
            "average_rating",
            "image_url",
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
