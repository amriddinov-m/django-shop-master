import django_filters

from product.models import Product, NewCategory


class ProductFilter(django_filters.FilterSet):
    id = django_filters.AllValuesMultipleFilter(field_name='id')

    # def filter_id(self, queryset, name, value):
    #     print(value)
    #     print(name)
    #     return queryset.filter()

    class Meta:
        model = Product
        fields = ['id', 'manufacturer', 'status', 'cat_one', 'in_stock', 'is_hot', 'article']


class CategoryFilter(django_filters.FilterSet):
    # def filter_id(self, queryset, name, value):
    #     print(value)
    #     print(name)
    #     return queryset.filter()

    class Meta:
        model = NewCategory
        fields = ['id', 'name', 'priority', 'is_main']

