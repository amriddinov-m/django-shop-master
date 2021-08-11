from rest_framework import serializers

from order.models import Order, Deliver, OrderItem
from product.models import Product
from user.models import User


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = 'id', 'title', 'article'


class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderProductSerializer(many=False, required=True)

    class Meta:
        model = OrderItem
        fields = 'product', 'price', 'count'


class OrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'first_name', 'last_name', 'phone', 'email'


class DeliverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deliver
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, required=False)
    user = OrderUserSerializer(many=False, required=False)
    deliver = DeliverSerializer(many=False, required=False)

    class Meta:
        model = Order
        fields = 'id', 'created', 'user', 'status', 'is_paid', 'products', \
                 'comments', 'last_changed_date', 'deliver', 'payment_method'

