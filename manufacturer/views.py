from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from manufacturer.filters import ManufacturerFilter
from manufacturer.models import Manufacturer
from manufacturer.serializer import ManufacturerSerializer
from other.views import CustomPagination


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_class = ManufacturerFilter
    filter_backends = (
        OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )
    ordering_fields = 'pk', 'place'
