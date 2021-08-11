import json
from rest_framework import viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order.filters import OrderFilter
from order.models import Order, Deliver, OrderItem
from order.serializer import OrderSerializer, DeliverSerializer
from other.views import CustomPagination


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_class = OrderFilter
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )
    ordering_fields = 'pk', 'created'

    def create(self, request, *args, **kwargs):
        try:
            products_list = json.loads(str(request.POST['products_list']).replace('\'', '"'))
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order = serializer.save(user_id=request.data['user'],
                                    deliver_id=request.data['deliver'])
            for product in products_list:
                item = OrderItem.objects.create(product_id=product['id'], price=product['price'], count=product['count'])
                order.products.add(item)
            order.products_init = True
            order.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as ex:
            print(ex)


class DeliverViewSet(viewsets.ModelViewSet):
    queryset = Deliver.objects.all()
    serializer_class = DeliverSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
