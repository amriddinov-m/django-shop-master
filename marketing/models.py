from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.translation import get_language
from modeltrans.fields import TranslationField
from unidecode import unidecode

from docs import PARTNERS_LOGO_SIZE, BANNERS_CHOICES
from marketing.choices import PAGE_POSITION_CHOICES, SOCIAL_CHOICES


class HotDeal(models.Model):
    product = models.ForeignKey('product.Product',
                                on_delete=models.CASCADE,
                                verbose_name='Товар')
    date_end = models.DateTimeField(auto_now_add=False,
                                    verbose_name='Дата окончание ')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Горячие предложения'
        verbose_name_plural = 'Горячие предложения'


class Slider(models.Model):
    title_1 = models.CharField(max_length=255,
                               null=True,
                               blank=True,
                               verbose_name='Заголовок 1')
    title_2 = models.CharField(max_length=255,
                               null=True,
                               blank=True,
                               verbose_name='Заголовок 2')
    sub_title = models.CharField(max_length=255,
                                 null=True,
                                 blank=True,
                                 verbose_name='Под Заголовок ')
    photo = models.ImageField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                              default=settings.NOIMAGE,
                              verbose_name='Картинка')
    btn_link = models.CharField(max_length=255,
                                null=True,
                                blank=True,
                                verbose_name='Ссылка')
    translation_fields = ('title_1', 'title_2', 'sub_title')
    i18n = TranslationField(fields=translation_fields)

    def __str__(self):
        return self.title_1_i18n

    def get_fields(self):
        return self.translation_fields

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдер'


class AdType(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип рекламы'
        verbose_name_plural = 'Тип рекламы'


class Banner(models.Model):
    photo = models.ImageField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                              default=settings.NOIMAGE,
                              verbose_name='Картинка')
    link = models.CharField(max_length=255,
                            verbose_name='Ссылка')
    ad_type = models.CharField(verbose_name='Тип рекламы',
                               max_length=255,
                               choices=BANNERS_CHOICES)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннер'


class Post(models.Model):
    photo = models.ImageField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                              default=settings.NOIMAGE,
                              verbose_name='Картинка')
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    short = models.TextField(null=True,
                             blank=True,
                             verbose_name='Короткое описание')
    content = RichTextUploadingField(null=True,
                                     blank=True,
                                     verbose_name='Контент')
    translation_fields = ('title', 'short', 'content')
    i18n = TranslationField(fields=translation_fields)
    slug = AutoSlugField(populate_from='get_slug',
                         max_length=255,
                         unique_with=('id',))

    def get_slug(self):
        return unidecode(self.title_ru)

    def get_fields(self):
        return self.translation_fields

    def __str__(self):
        return self.title_i18n

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блог'


class Coupon(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Название купона',
                             null=True,
                             blank=True)
    amount = models.BigIntegerField(default=0,
                                    verbose_name='Сумма')
    hash = models.CharField(max_length=255,
                            verbose_name='Код/хеш',
                            unique=True)
    expire_date = models.DateTimeField(auto_now_add=False,
                                       null=True,
                                       blank=True,
                                       verbose_name='Дата окончание')
    created = models.DateTimeField(auto_now_add=True)
    translation_fields = ('title', )
    i18n = TranslationField(fields=translation_fields)

    def __str__(self):
        return self.title_i18n

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        pass

    def get_fields(self):
        return self.translation_fields

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купон'


class Page(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    keywords = models.TextField(null=True,
                                blank=True,
                                verbose_name='Ключевые слова SEO')
    meta_title = models.CharField(max_length=255,
                                  verbose_name='Заголовок окна',
                                  null=True,
                                  blank=True)
    description = models.TextField(null=True,
                                   blank=True,
                                   verbose_name='Описание SEO')
    content = RichTextUploadingField(verbose_name='Содержание страницы')
    position = models.CharField(max_length=255,
                                choices=PAGE_POSITION_CHOICES,
                                verbose_name='Расположение')
    priority = models.IntegerField(default=0,
                                   verbose_name='Приоритет')
    translation_fields = ('title', 'keywords', 'meta_title', 'description', 'content')
    i18n = TranslationField(fields=translation_fields)
    slug = AutoSlugField(populate_from='get_slug',
                         max_length=255,
                         unique_with=('id',))

    def get_slug(self):
        return unidecode(self.title_ru)

    def __str__(self):
        return self.title_i18n

    def get_fields(self):
        return self.translation_fields

    class Meta:
        verbose_name = 'Страницы'
        verbose_name_plural = 'Страницы'


class Partner(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    photo = models.ImageField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                              default=settings.NOIMAGE,
                              verbose_name='Картинка',
                              help_text='Рекомендованный размер картинки {}'.format(PARTNERS_LOGO_SIZE))
    priority = models.IntegerField(default=0)
    has_content = models.BooleanField(default=False,
                                      verbose_name='Есть контент?')
    content = RichTextUploadingField(null=True,
                                     blank=True)
    translation_fields = ('content', )
    i18n = TranslationField(fields=translation_fields)
    slug = AutoSlugField(populate_from='get_slug',
                         max_length=255,
                         unique_with=('id',))

    def get_slug(self):
        return unidecode(self.title)

    def __str__(self):
        return self.title

    def get_fields(self):
        return self.translation_fields

    class Meta:
        verbose_name = 'Партнеры'
        verbose_name_plural = 'Партнеры'


class Certificate(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    photo = models.ImageField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                              default=settings.NOIMAGE,
                              verbose_name='Картинка')
    description = models.TextField(null=True,
                                   blank=True)
    translation_fields = ('title', 'description')
    i18n = TranslationField(fields=translation_fields)
    slug = AutoSlugField(populate_from='get_slug',
                         max_length=255,
                         unique_with=('id',))

    def get_slug(self):
        return unidecode(self.title_ru)

    def __str__(self):
        return self.title_i18n

    def get_fields(self):
        return self.translation_fields

    class Meta:
        verbose_name = 'Сертификаты'
        verbose_name_plural = 'Сертификаты'


class Social(models.Model):
    link = models.CharField(max_length=255,
                            verbose_name='Заголовок')
    icon = models.CharField(max_length=255,
                            verbose_name='Соц. сеть',
                            choices=SOCIAL_CHOICES)

    class Meta:
        verbose_name = 'Социальные сети'
        verbose_name_plural = 'Социальные сети'


class Review(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    content = models.TextField()
    user = models.ForeignKey('user.User',
                             on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзывы'

