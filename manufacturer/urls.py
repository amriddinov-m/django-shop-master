from rest_framework import routers

from manufacturer.views import ManufacturerViewSet

router = routers.SimpleRouter()
router.register(r'manufacturers', ManufacturerViewSet)
urlpatterns = router.urls
