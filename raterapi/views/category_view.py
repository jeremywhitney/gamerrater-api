from rest_framework import serializers, viewsets
from raterapi.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
