from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from raterapi.models import Picture, Game
import uuid
import base64
from django.core.files.base import ContentFile


class PictureSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = Picture
        fields = ("id", "game", "action_pic")


class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    def create(self, request, *args, **kwargs):
        # Create a new instance of the game picture model
        game_picture = Picture()

        # Extract and decode the base64 image
        format, imgstr = request.data["game_image"].split(";base64,")
        ext = format.split("/")[-1]
        data = ContentFile(
            base64.b64decode(imgstr),
            name=f'{request.data["game_id"]}-{uuid.uuid4()}.{ext}',
        )

        # Set the image property of the game picture instance
        game_picture.action_pic = data
        game_picture.game_id = request.data["game_id"]

        # Save the data to the database
        game_picture.save()

        # Update the Game model's image_url field
        game = Game.objects.get(id=request.data["game_id"])
        game.image_url = game_picture.action_pic.url
        # Verify file is saved
        print(f'File saved at: {game.image_url}')
        game.save()

        # Serialize the saved picture instance and return a response
        serializer = self.get_serializer(game_picture)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
