from datetime import datetime

from rest_framework import serializers

from marketing.models import HotDeal, Slider, AdType, Banner, Post, Coupon


class HotDealSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = HotDeal
        fields = 'id', 'product', 'date'

    def get_date(self, obj):
        if obj.date_end:
            return datetime.strftime(obj.date_end, '%Y/%m/%d %H:%M:%S')
        else:
            return obj.date_end


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'


class AdTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdType
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
