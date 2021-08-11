from rest_framework import routers

from payment.views import PaymentViewSet

router = routers.SimpleRouter()
router.register(r'payments', PaymentViewSet)
urlpatterns = router.urls
