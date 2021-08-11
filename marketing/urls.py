from rest_framework import routers

from marketing.views import HotDealViewSet, SliderViewSet, AdTypeViewSet,\
    BannerViewSet, PostViewSet, CouponViewSet

router = routers.SimpleRouter()
router.register(r'hot_deals', HotDealViewSet)
router.register(r'banners', BannerViewSet)
router.register(r'ad_types', AdTypeViewSet)
router.register(r'sliders', SliderViewSet)
router.register(r'posts', PostViewSet)
router.register(r'coupons', CouponViewSet)
urlpatterns = router.urls
