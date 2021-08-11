from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from marketing.models import HotDeal, Banner, AdType, Slider, Post, Coupon
from marketing.serializer import HotDealSerializer, BannerSerializer, SliderSerializer, AdTypeSerializer, \
    PostSerializer, CouponSerializer
from other.views import CustomPagination


class HotDealViewSet(viewsets.ModelViewSet):
    queryset = HotDeal.objects.all()
    serializer_class = HotDealSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]


class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]


class AdTypeViewSet(viewsets.ModelViewSet):
    queryset = AdType.objects.all()
    serializer_class = AdTypeSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]


class SliderViewSet(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
