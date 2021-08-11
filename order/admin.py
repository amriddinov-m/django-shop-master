from django.contrib import admin

from dsshop.settings import MODELTRANS_AVAILABLE_LANGUAGES
from order.models import Order, Deliver, ProductCall, ProductMailing


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Deliver)
class DeliverAdmin(admin.ModelAdmin):
    list_display = 'title_i18n', 'price'
    translation_fields = []
    for p in Deliver().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.append('price')

    fields = translation_fields


@admin.register(ProductCall)
class ProductCallAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductMailing)
class ProductMailingAdmin(admin.ModelAdmin):
    pass
