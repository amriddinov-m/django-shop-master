from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from tabbed_admin import TabbedModelAdmin

from dsshop.settings import MODELTRANS_AVAILABLE_LANGUAGES
from product.models import Product, NewCategory, ProductPhoto, ProductReview, ProductFunction, ProductService, \
    ProductDocument, ProductProperty, ProductSpecification, ProductComponent, ProductBrand, ProductImage, \
    ProductPickupPoint, ProductPage, ProductVideo


class ProductPhotoInline(admin.TabularInline):
    model = ProductPhoto
    min_num = 2
    extra = 0


@admin.register(Product)
class ProductAdmin(TabbedModelAdmin):
    list_display = 'id', 'title', 'manufacturer', 'article', 'price', 'status', 'in_stock', 'is_hot'
    autocomplete_fields = ['manufacturer', ]
    list_filter = 'is_hot', 'in_stock', 'status'
    search_fields = 'title', 'keywords'
    filter_horizontal = 'cat_one',
    readonly_fields = 'last_price_update', 'show_price'
    translation_fields = []
    for p in Product().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.extend(['guaranty', 'article', 'model'])
    tab_overview = (
        (None, {
            'fields': (*translation_fields,)
        }),

    )
    price_overview = (
        (None, {
            'fields': ('price', 'discount', 'discount_type', 'last_price_update', 'show_price')
        }),
    )
    cat_overview = (
        (None, {
            'fields': ('manufacturer', 'cat_one'),
        }),
    )
    flags_overview = (
        (None, {
            'fields': ('in_stock', 'is_hot', 'status')
        }),
    )
    photo_inline = (
        ProductPhotoInline,
    )
    tabs = [
        ('Основная информация', tab_overview),
        ('Категории', cat_overview),
        ('Цены', price_overview),
        ('Картинки', photo_inline),
        ('Галочки', flags_overview),
    ]


@admin.register(NewCategory)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = 'tree_actions', 'indented_title', 'name_i18n', 'is_main'
    search_fields = 'name',
    translation_fields = []
    for p in NewCategory().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.extend(['priority', 'parent', 'icon', 'is_main'])
    fields = translation_fields


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductFunction)
class ProductFunctionAdmin(admin.ModelAdmin):
    translation_fields = []
    for p in ProductFunction().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.extend(['photo', 'brand_name'])
    fields = translation_fields


@admin.register(ProductService)
class ProductServiceAdmin(admin.ModelAdmin):
    translation_fields = []
    for p in ProductService().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.extend(['name', 'type', 'status', 'pay_cash', 'online_cash', 'price', 'currency',
                               'false_discount', 'guarantee'])
    fields = translation_fields


@admin.register(ProductDocument)
class ProductDocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductProperty)
class ProductProperty(admin.ModelAdmin):
    translation_fields = []
    for p in ProductProperty().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.extend(['color'])
    fields = translation_fields


@admin.register(ProductSpecification)
class ProductSpecification(admin.ModelAdmin):
    translation_fields = []
    for p in ProductSpecification().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.extend(['measurement', 'type', 'photo'])
    fields = translation_fields


@admin.register(ProductComponent)
class ProductComponent(admin.ModelAdmin):
    translation_fields = []
    for p in ProductComponent().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.extend(['brand_name', 'photo'])
    fields = translation_fields


@admin.register(ProductBrand)
class ProductBrand(admin.ModelAdmin):
    translation_fields = []
    for p in ProductBrand().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.extend(['title', 'type', 'photo'])
    fields = translation_fields


@admin.register(ProductImage)
class ProductImage(admin.ModelAdmin):
    pass


@admin.register(ProductPickupPoint)
class ProductPickupPoint(admin.ModelAdmin):
    translation_fields = []
    for p in ProductPickupPoint().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.extend(['card', 'status'])
    fields = translation_fields


@admin.register(ProductPage)
class ProductPage(admin.ModelAdmin):
    translation_fields = []
    for p in ProductPage().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.extend(['parent_page', 'status', 'display', 'priority'])
    fields = translation_fields


@admin.register(ProductVideo)
class ProductVideo(admin.ModelAdmin):
    pass
