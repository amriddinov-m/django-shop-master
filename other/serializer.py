from rest_framework import serializers

from other.models import Project
from product.serializer import ProductCategorySerializer


class ProjectSerializer(serializers.ModelSerializer):
    cat = ProductCategorySerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = 'id', 'cat', 'rate', 'rate2',

