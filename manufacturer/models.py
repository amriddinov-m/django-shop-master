from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from modeltrans.fields import TranslationField
from unidecode import unidecode

from product.choices import DISCOUNT_TYPE_CHOICES


class Manufacturer(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название')
    icon = models.ImageField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                             default=settings.NOIMAGE,
                             verbose_name='Иконка/Картинка')
    in_top = models.BooleanField(default=False,
                                 verbose_name='Наверху')
    slug = AutoSlugField(populate_from='get_slug',
                         max_length=255,
                         unique_with=('id',))
    description = RichTextUploadingField(null=True,
                                         blank=True,
                                         verbose_name='Описание')
    discount_type = models.CharField(max_length=255,
                                     verbose_name='Тип скидки',
                                     choices=DISCOUNT_TYPE_CHOICES,
                                     default='none')
    place = models.IntegerField(default=0,
                                verbose_name='Позиция')

    translation_fields = ('description',)
    i18n = TranslationField(fields=translation_fields)

    def get_slug(self):
        return unidecode(self.name)

    def __str__(self):
        return self.name_i18n

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производитель'

    def get_fields(self):
        return self.translation_fields
