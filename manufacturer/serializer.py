from rest_framework import serializers

from conf import SERVER_URI
from manufacturer.models import Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Manufacturer
        fields = 'id', 'name', 'icon', 'in_top', 'place'

    def get_icon(self, obj):
        if obj.icon:
            return str(SERVER_URI) + str(obj.icon.url).replace('media/media', 'media')
