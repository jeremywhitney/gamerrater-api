from rest_framework import serializers, viewsets
from raterapi.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            "id",
            "player",
            "game",
            "rating",
        )
        read_only_fields = ("player",)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        # Check if the user already rated the game
        if Rating.objects.filter(
            player=self.request.user, game=serializer.validated_data["game"]
        ).exists():
            raise serializers.ValidationError("You have already rated this game.")
        # Save the new rating
        serializer.save(player=self.request.user)

    def perform_update(self, serializer):
        # For updating an existing rating, no need to check uniqueness
        serializer.save()
