import django_filters

from manufacturer.models import Manufacturer


class ManufacturerFilter(django_filters.FilterSet):

    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'in_top', 'place']


