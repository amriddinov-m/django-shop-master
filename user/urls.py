from rest_framework import routers

from user.views import UserViewSet, GroupViewSet, UserAddressViewSet

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)
router.register(r'group', GroupViewSet)
router.register(r'user_address', UserAddressViewSet)
urlpatterns = router.urls
