from django.urls import path

from frontend.views import HomeView, CategoryDetailView, ProductDetailView, SetLanguage, RegistrationView, \
    CertificateView, PageView, PartnerView, CartView, ReviewView, OrderView, PaymentView, RegisterView, SearchView, \
    SuccessView, BlogListView, BlogDetailView, LoginView, ProfileView, ProfileEditView, OrderHistoryView, TestView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/detail/<str:slug>/', CategoryDetailView.as_view(), name='category-detail-frontend'),
    path('product/<str:slug>/', ProductDetailView.as_view(), name='product-detail-frontend'),
    path('change/language/', SetLanguage.as_view(), name='set-language'),
    path('registration/', RegistrationView.as_view(), name='registration-view'),
    path('certificate/', CertificateView.as_view(), name='certificate-view'),
    path('page/<str:slug>/', PageView.as_view(), name='page-view'),
    path('partner/<str:slug>/', PartnerView.as_view(), name='partner-view'),
    path('cart/', CartView.as_view(), name='cart-view'),
    path('reviews/', ReviewView.as_view(), name='reviews-view'),
    path('order/', OrderView.as_view(), name='order-view'),
    path('payment/', PaymentView.as_view(), name='payment-view'),
    path('blog/', BlogListView.as_view(), name='blog-view'),
    path('blog/<str:slug>/', BlogDetailView.as_view(), name='blog-detail-view'),
    path('login/', LoginView.as_view(), name='login-view'),
    path('profile/', ProfileView.as_view(), name='profile-view'),
    path('profile/update', ProfileEditView.as_view(), name='profile-update-view'),
    path('profile/orders', OrderHistoryView.as_view(), name='profile-orders-view'),
    path('register/', RegisterView.as_view(), name='register-view'),
    path('search/', SearchView.as_view(), name='search-view'),
    path('success/', SuccessView.as_view(), name='success-view'),
    path('test/', TestView.as_view(), name=''),


]
