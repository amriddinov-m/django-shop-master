from django.contrib import admin

from dsshop.settings import MODELTRANS_AVAILABLE_LANGUAGES
from marketing.models import HotDeal, Banner, AdType, Slider, Partner, Page, Certificate, Social, Review, Post


@admin.register(HotDeal)
class HotDealAdmin(admin.ModelAdmin):
    autocomplete_fields = ['product', ]


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    actions = None

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AdType)
class AdTypeAdmin(admin.ModelAdmin):

    actions = None

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    translation_fields = []
    for p in Slider().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.extend(['photo', 'btn_link'])
    fields = translation_fields


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    pass


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    translation_fields = []
    for p in Page().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.extend(['position', 'priority'])
    fields = translation_fields


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    translation_fields = []
    for p in Certificate().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.append('photo')

    fields = translation_fields


@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    translation_fields = []
    for p in Post().get_fields():
        for lang in MODELTRANS_AVAILABLE_LANGUAGES:
            translation_fields.append(str(p) + "_" + str(lang))
    translation_fields.append('photo')

    fields = translation_fields
