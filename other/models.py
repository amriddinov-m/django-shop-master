from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from thumbnail_maker.fields import ImageWithThumbnailsField


class Project(models.Model):
    cat = models.ManyToManyField('product.NewCategory',
                                 verbose_name='Категории на главной страницы')
    rate = models.FloatField(default=0,
                             verbose_name='Курс доллара')
    rate2 = models.FloatField(default=0,
                              verbose_name='Курс доллара2')

    def __str__(self):
        return "Настройки"

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

