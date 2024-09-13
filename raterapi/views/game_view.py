from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Game, Category
from django.contrib.auth.models import User


class GameView(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        game = Game()
        game.created_by = request.auth.user
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.year_released = request.data["year_released"]
        game.number_of_players = request.data["number_of_players"]
        game.estimated_time_to_play = request.data["estimated_time_to_play"]
        game.age_recommendation = request.data["age_recommendation"]

        try:
            game.save()
            game.categories.set(request.data["categories"])
            serializer = GameSerializer(game, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- JSON serialized updated instance or error
        """
        try:
            game = Game.objects.get(pk=pk)

            if request.auth.user != game.created_by:
                return Response(
                    {"detail": "You do not have permission to edit this game."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            game.title = request.data["title"]
            game.description = request.data["description"]
            game.designer = request.data["designer"]
            game.year_released = request.data["year_released"]
            game.number_of_players = request.data["number_of_players"]
            game.estimated_time_to_play = request.data["estimated_time_to_play"]
            game.age_recommendation = request.data["age_recommendation"]

            game.save()

            if "categories" in request.data:
                game.categories.set(request.data["categories"])

            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Game.DoesNotExist:
            return Response(
                {"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            return Response({"reason": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            games = Game.objects.all()
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class GameCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    created_by = GameCreatorSerializer(many=False)
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
