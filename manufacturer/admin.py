from django.contrib import admin

from dsshop.settings import MODELTRANS_AVAILABLE_LANGUAGES
from manufacturer.models import Manufacturer


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    translation_fields = []
    for p in Manufacturer().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.extend(['name', 'icon', 'in_top', 'discount_type', 'place'])
    fields = translation_fields
    search_fields = 'name',
