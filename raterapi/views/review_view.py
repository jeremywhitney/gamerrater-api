from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from raterapi.models import Review
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class ReviewSerializer(serializers.ModelSerializer):
    player = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "player",
            "game",
            "review_text",
            "created_at",
            "updated_at",
        ]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all().order_by("-created_at")
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        queryset = super().get_queryset()
        game_id = self.request.query_params.get("gameId")
        if game_id:
            queryset = queryset.filter(game_id=game_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)  # Automatically set the player field
