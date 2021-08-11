from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from other.models import Project
from other.views import CustomPagination
from product.filters import ProductFilter, CategoryFilter
from product.models import Product, NewCategory, ProductPhoto
from product.serializer import ProductSerializer, NewCategorySerializer, ProductPhotoSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('cat_one')
    serializer_class = ProductSerializer
    filter_class = ProductFilter
    filter_backends = (
        OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )
    pagination_class = CustomPagination
    ordering_fields = 'pk',
    search_fields = 'title', 'keywords'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.prefetch_related('cat_one', 'photos')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = NewCategory.objects.filter(is_main=True).select_related()
    pagination_class = CustomPagination
    serializer_class = NewCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_class = CategoryFilter
    filter_backends = (
        OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )
    ordering_fields = 'pk', 'priority',
    search_fields = 'title', 'keywords'


class ProductPhotoViewSet(viewsets.ModelViewSet):
    queryset = ProductPhoto.objects.all()
    pagination_class = CustomPagination
    serializer_class = ProductPhotoSerializer
    permission_classes = [IsAuthenticated]


class MainProductAPI(viewsets.ViewSet):

    def list(self, request):
        project = Project.objects.first()
        products = Product.objects.filter(cat_one__id__in=[project.first_id, project.second_id])
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
