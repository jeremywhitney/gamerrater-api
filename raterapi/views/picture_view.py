from rest_framework import serializers, viewsets
from raterapi.models import Picture


class PictureSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = Picture
        fields = ("id", "game", "action_pic")


class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
