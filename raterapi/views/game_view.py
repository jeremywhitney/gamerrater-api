from rest_framework import serializers, viewsets
from raterapi.models import Game, Category
from rest_framework.permissions import IsAuthenticated


class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    created_by = serializers.ReadOnlyField(
        source="created_by.username"
    )  # Only display user, not accept it in input

    categories = GameCategorySerializer(many=True)

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
        serializer.save(created_by=self.request.user)
