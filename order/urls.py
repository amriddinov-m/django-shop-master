from rest_framework import routers

from order.views import OrderViewSet, DeliverViewSet

router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet)
router.register(r'deliver', DeliverViewSet)
urlpatterns = router.urls
