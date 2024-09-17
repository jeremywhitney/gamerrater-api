from rest_framework import serializers, viewsets
from raterapi.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "player",
            "game",
            "rating",
            "review_text",
            "created_at",
            "updated_at",
        ]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by("-created_at")
    serializer_class = ReviewSerializer
