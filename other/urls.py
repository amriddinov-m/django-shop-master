from rest_framework import routers

from product.views import ProductViewSet, CategoryViewSet, ProductPhotoViewSet, MainProductAPI

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'products_photos', ProductPhotoViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'main_product', MainProductAPI, basename='main_product')
urlpatterns = router.urls
