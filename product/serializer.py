from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from conf import SERVER_URI
from product.models import Product, NewCategory, ProductPhoto


class SubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewCategory
        fields = 'id', 'name', 'priority', 'icon'


class SubCategorySerializer(serializers.ModelSerializer):
    sub = SubSubCategorySerializer(many=True, required=False)

    class Meta:
        model = NewCategory
        fields = 'id', 'name', 'priority', 'icon', 'sub'


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = '__all__'


class RecursiveField1(serializers.Serializer):

    def to_native(self, value):
        return NewCategorySerializer(value, context={"parent": self.parent.object, "parent_serializer": self.parent})


class NewCategorySerializer(serializers.ModelSerializer):
    sub = SubCategorySerializer(many=True, required=False)

    class Meta:
        model = NewCategory
        fields = 'id', 'name', 'priority', 'icon', 'sub'


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = NewCategory
        fields = 'id', 'name'


class ProductSerializer(serializers.ModelSerializer):

    # cat_one = serializers.PrimaryKeyRelatedField(many=True,
    #                                              queryset=NewCategory.objects.all())

    # cat_one = ProductCategorySerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

    # def get_thumb200(self, obj):
    #     arr = []
    #     for i in obj.photos.all():
    #         thumb = get_thumbnail(i.photo, '200x200')
    #         arr.append(SERVER_URI + str(thumb.url))
    #     return arr
    #
    # def get_thumb50(self, obj):
    #     arr = []
    #     for i in obj.photos.all():
    #         thumb = get_thumbnail(i.photo, '50x50')
    #         arr.append(SERVER_URI + str(thumb.url))
    #     return arr


