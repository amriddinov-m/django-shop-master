import django_filters

from order.models import Order


class OrderFilter(django_filters.FilterSet):

    class Meta:
        model = Order
        fields = ['status', 'user', 'is_paid', 'deliver']
