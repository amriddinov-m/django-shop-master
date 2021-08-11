"""dsshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.utils import translation
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

from frontend.views import cart_action, change_currency
from manufacturer.urls import router as manufacturer_router
from order.urls import router as order_router
from payment.urls import router as payment_router
from payment.views import jsonrpc, ApelsinEndPoint
from product.urls import router as product_router
from user.urls import router as user_router
from marketing.urls import router as marketing_router
from other.urls import router as other_router

from dsshop.router import DefaultRouter

router = DefaultRouter()
router.extend(manufacturer_router)
router.extend(order_router)
router.extend(payment_router)
router.extend(product_router)
router.extend(user_router)
router.extend(marketing_router)
router.extend(other_router)

urlpatterns = [
                  path('grappelli/', include('grappelli.urls')),
                  path('admin/', admin.site.urls),
                  url(r'api/v1/', include(router.urls)),
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
                  url(r'^rest-auth/', include('rest_auth.urls')),
                  url(r'^jsonrpc/', jsonrpc, name='jsonrpc'),
                  url(r'^apelsin/', ApelsinEndPoint.as_view(), name='apelsin_endpoint'),

                  path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
                  path('cart_action/', cart_action, name='cart-action'),
                  path('currency/change/', change_currency, name='change-currency-view'),
                  path('accounts/', include('django.contrib.auth.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += i18n_patterns(
    url('', include('frontend.urls')),
)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),

                      # For django versions before 2.0:
                      # url(r'^__debug__/', include(debug_toolbar.urls)),

                  ] + urlpatterns