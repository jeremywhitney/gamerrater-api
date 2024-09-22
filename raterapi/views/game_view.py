from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from raterapi.models import Game, Category
from django.contrib.auth.models import User
from django.db.models import F, Q


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

    def list(self, request):
        queryset = self.queryset
        search_text = self.request.query_params.get("q", None)
        order_by = self.request.query_params.get("orderby", None)

        if search_text is not None:
            queryset = queryset.filter(
                Q(title__icontains=search_text)
                | Q(description__icontains=search_text)
                | Q(designer__icontains=search_text)
            )

        if order_by:
            if order_by == "year":
                queryset = queryset.order_by(F("year_released").desc(nulls_last=True))
            elif order_by == "time":
                queryset = queryset.order_by(
                    F("estimated_time_to_play").desc(nulls_last=True)
                )
            elif order_by == "designer":
                queryset = queryset.order_by("designer")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
