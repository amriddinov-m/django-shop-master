import django
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from modeltrans.fields import TranslationField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from thumbnail_maker.fields import ImageWithThumbnailsField
from unidecode import unidecode
from conf import SERVER_URI
from product.choices import DISCOUNT_TYPE_CHOICES, STATUS_TYPE_CHOICES, SERVICES_TYPE_CHOICES, CURRENCY_TYPE_CHOICES, \
    LANGUAGE_TYPE_CHOICES, TOP_TYPE_CHOICES, PARENT_TYPE_CHOICES, PAGE_TYPE_CHOICES


class NewCategory(MPTTModel):
    name = models.CharField(max_length=255,
                            verbose_name='Название')
    priority = models.IntegerField(default=0,
                                   verbose_name='Позиция')
    icon = models.ImageField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                             default=settings.NOIMAGE,
                             verbose_name='Иконка/Картинка')
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='sub',
                            verbose_name='Родительская категория')
    is_main = models.BooleanField(default=False,
                                  verbose_name='Основная')
    translation_fields = ('name',)
    i18n = TranslationField(fields=translation_fields)
    slug = AutoSlugField(populate_from='get_slug',
                         max_length=255,
                         unique_with=('id',))

    def get_fields(self):
        return self.translation_fields

    def get_slug(self):
        return unidecode(self.name_ru)

    def __str__(self):
        return self.name_i18n

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категория товаров'


class ProductPhoto(models.Model):
    product = models.ForeignKey('Product',
                                on_delete=models.CASCADE,
                                related_name='photos',
                                verbose_name='Товар')
    photo = ImageWithThumbnailsField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                                     default=settings.NOIMAGE,
                                     auto_save_thumb=True,
                                     thumbs=('200x200', '50x50'))

    def __str__(self):
        return str(SERVER_URI) + str(self.photo.url)


class Product(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    manufacturer = models.ForeignKey('manufacturer.Manufacturer',
                                     on_delete=models.PROTECT,
                                     null=True,
                                     blank=True,
                                     verbose_name='Производитель')
    status = models.BooleanField(default=False,
                                 verbose_name='Статус')
    title = models.CharField(max_length=255,
                             verbose_name='Название')
    description = RichTextUploadingField(null=True,
                                         blank=True,
                                         verbose_name='Описание')
    price = models.FloatField(default=0,
                              verbose_name='Цена')
    discount = models.FloatField(default=0,
                                 verbose_name='Скидка')
    discount_type = models.CharField(max_length=255,
                                     verbose_name='Тип скидки',
                                     choices=DISCOUNT_TYPE_CHOICES,
                                     default='none')
    guaranty = models.CharField(max_length=2,
                                verbose_name='Гарантия (месяц)',
                                null=True,
                                blank=True)
    keywords = models.TextField(null=True,
                                blank=True,
                                verbose_name='Ключевые слова')
    cat_one = models.ManyToManyField('NewCategory',
                                     related_name='cat_one',
                                     verbose_name='Категория',
                                     null=True,
                                     blank=True)

    in_stock = models.BooleanField(default=False,
                                   verbose_name='В складе')
    article = models.CharField(max_length=255,
                               verbose_name='Артикул',
                               null=True,
                               blank=True)
    is_hot = models.BooleanField(default=False,
                                 verbose_name='Популярный товар')
    model = models.CharField(max_length=255,
                             null=True,
                             blank=True,
                             verbose_name='Модель')
    short = models.TextField(null=True,
                             blank=True,
                             verbose_name='Короткое описание')
    last_price_update = models.DateTimeField(auto_now_add=True,
                                             verbose_name='Последнее обновление цены')
    translation_fields = ('title', 'description', 'short', 'keywords')
    slug = AutoSlugField(populate_from='get_slug',
                         max_length=255,
                         unique_with=('id',))
    i18n = TranslationField(fields=translation_fields)
    show_price = models.FloatField(default=0,
                                   verbose_name='Цена после скидок',
                                   editable=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.discount:
            if self.discount_type == 'percent':
                self.show_price = float(self.price) - (float(self.price) * float(self.discount) / 100)
            else:
                self.show_price = float(self.price) - float(self.discount)
        else:
            self.show_price = self.price
        super(Product, self).save()

    def get_slug(self):
        return unidecode(self.title_ru)

    def __str__(self):
        return self.title_i18n

    def get_fields(self):
        return self.translation_fields

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'


class ProductReview(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    content = models.TextField(null=True,
                               blank=True)
    user = models.ForeignKey('user.User',
                             on_delete=models.PROTECT,
                             null=True,
                             blank=True)
    product = models.ForeignKey('Product',
                                on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Отзывы товаров'
        verbose_name_plural = 'Отзывы товаров'


class ProductFunction(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')

    photo = ImageWithThumbnailsField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                                     default=settings.NOIMAGE,
                                     auto_save_thumb=True,
                                     thumbs=('200x200', '50x50'))

    brand_name = models.ForeignKey('ProductBrand',
                                   on_delete=models.PROTECT,
                                   verbose_name='Бренд')

    description = RichTextUploadingField(null=True,
                                         blank=True,
                                         verbose_name='Описание')
    translation_fields = ('title', 'description')
    i18n = TranslationField(fields=translation_fields)

    def __str__(self):
        return self.title_i18n

    class Meta:
        verbose_name = 'Функция продуктов'
        verbose_name_plural = 'Функции продуктов'

    def get_fields(self):
        return self.translation_fields


class ProductService(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название')
    type = models.CharField(max_length=255,
                            verbose_name='Тип',
                            choices=SERVICES_TYPE_CHOICES,
                            default='none')
    status = models.CharField(max_length=255,
                              verbose_name='Активен',
                              choices=STATUS_TYPE_CHOICES)
    pay_cash = models.BooleanField(default=False)
    online_cash = models.BooleanField(default=False,
                                      verbose_name='Онлайн оплата')
    text = RichTextUploadingField(null=True,
                                  blank=True,
                                  verbose_name='Описание')
    price = models.FloatField(default=0,
                              verbose_name='Цена')
    currency = models.CharField(max_length=255,
                                verbose_name='Валюта',
                                choices=CURRENCY_TYPE_CHOICES,
                                default='none')
    false_discount = models.FloatField(verbose_name='Фальш скидка')
    guarantee = models.FloatField(verbose_name='Гарантия')
    keywords = models.TextField(null=True,
                                blank=True,
                                verbose_name='Ключевые слова')
    description = models.TextField(null=True,
                                   blank=True,
                                   verbose_name='Описание')
    translation_fields = ('text', 'keywords', 'description')
    i18n = TranslationField(fields=translation_fields)

    def __str__(self):
        return self.name_i18n

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def get_fields(self):
        return self.translation_fields


class ProductDocument(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название')
    type = models.CharField(max_length=255,
                            verbose_name='Тип',
                            choices=SERVICES_TYPE_CHOICES,
                            default='none')
    brand_name = models.ForeignKey('ProductBrand',
                                   on_delete=models.PROTECT,
                                   verbose_name='Бренд')
    lineup = models.CharField(max_length=255,
                              verbose_name='Модельный ряд',
                              choices=TOP_TYPE_CHOICES,
                              default='none')
    language = models.CharField(max_length=255,
                                verbose_name='Язык',
                                choices=LANGUAGE_TYPE_CHOICES,
                                default='none')
    description = models.TextField(null=True,
                                   blank=True,
                                   verbose_name='Текст')
    photo = ImageWithThumbnailsField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                                     default=settings.NOIMAGE,
                                     auto_save_thumb=True,
                                     thumbs=('200x200', '50x50'))

    file = models.FileField(upload_to='file',
                            verbose_name='Файл')
    show_page = models.BooleanField(default=False,
                                    verbose_name='Показывать на странице бренда')
    show_brand = models.BooleanField(default=False,
                                     verbose_name='Показывать на каждом товаре бренда')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class ProductProperty(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    color = ColorField(default='#FF0000')
    translation_fields = ('title',)
    i18n = TranslationField(fields=translation_fields)

    def __str__(self):
        return self.title_i18n

    class Meta:
        verbose_name = 'Свойство'
        verbose_name_plural = 'Свойства'

    def get_fields(self):
        return self.translation_fields


class ProductComponent(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    text = models.CharField(max_length=255,
                            verbose_name='Описание')
    brand_name = models.ForeignKey('ProductBrand',
                                   on_delete=models.PROTECT,
                                   verbose_name='Бренд')
    photo = ImageWithThumbnailsField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                                     default=settings.NOIMAGE,
                                     auto_save_thumb=True,
                                     thumbs=('200x200', '50x50'))
    translation_fields = ('title', 'text')
    i18n = TranslationField(fields=translation_fields)

    def __str__(self):
        return self.title_i18n

    class Meta:
        verbose_name = 'Комплектующий'
        verbose_name_plural = 'Комплектующие'

    def get_fields(self):
        return self.translation_fields


class ProductSpecification(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    value = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    measurement = models.CharField(max_length=255,
                                   verbose_name='Единица измерения')
    type = models.CharField(max_length=255,
                            verbose_name='Тип',
                            choices=SERVICES_TYPE_CHOICES,
                            default='none')
    photo = ImageWithThumbnailsField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                                     default=settings.NOIMAGE,
                                     auto_save_thumb=True,
                                     thumbs=('200x200', '50x50'))
    translation_fields = ('title', 'value')
    i18n = TranslationField(fields=translation_fields)

    def __str__(self):
        return self.title_i18n

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def get_fields(self):
        return self.translation_fields


class ProductBrand(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    type = models.CharField(max_length=255,
                            verbose_name='Топ',
                            choices=TOP_TYPE_CHOICES,
                            default='none')
    photo = ImageWithThumbnailsField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                                     default=settings.NOIMAGE,
                                     auto_save_thumb=True,
                                     verbose_name='Логотип',
                                     thumbs=('200x200', '50x50'))
    description = RichTextUploadingField(null=True,
                                         blank=True,
                                         verbose_name='Описание')

    translation_fields = ('description',)
    i18n = TranslationField(fields=translation_fields)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def get_fields(self):
        return self.translation_fields


class ProductImage(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Название')
    brand_name = models.ForeignKey('ProductBrand',
                                   on_delete=models.PROTECT,
                                   verbose_name='Бренд')
    lineup = models.CharField(max_length=255,
                              verbose_name='Модельный ряд',
                              choices=TOP_TYPE_CHOICES,
                              default='none')
    photo = ImageWithThumbnailsField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                                     default=settings.NOIMAGE,
                                     auto_save_thumb=True,
                                     verbose_name='Изображение',
                                     thumbs=('200x200', '50x50'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'


class ProductPickupPoint(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    text = RichTextUploadingField(null=True,
                                  blank=True,
                                  verbose_name='Текст')
    address = RichTextUploadingField(null=True,
                                     blank=True,
                                     verbose_name='Адрес')
    timetable = RichTextUploadingField(null=True,
                                       blank=True,
                                       verbose_name='Рассписание')
    payment = RichTextUploadingField(null=True,
                                     blank=True,
                                     verbose_name='Оплата')
    card = models.TextField(null=True,
                            blank=True,
                            verbose_name='Карта')
    status = models.CharField(max_length=255,
                              verbose_name='Оплата',
                              choices=STATUS_TYPE_CHOICES)
    translation_fields = ('title', 'text', 'address', 'timetable', 'payment')
    i18n = TranslationField(fields=translation_fields)

    def __str__(self):
        return self.title_i18n

    class Meta:
        verbose_name = 'Пункт выдачи'
        verbose_name_plural = 'Пункт выдачи'

    def get_fields(self):
        return self.translation_fields


class ProductPage(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    parent_page = models.CharField(max_length=255,
                                   verbose_name='Родительская страница',
                                   choices=PARENT_TYPE_CHOICES)
    status = models.CharField(max_length=255,
                              verbose_name='Активен',
                              choices=STATUS_TYPE_CHOICES)
    display = models.CharField(max_length=255,
                               verbose_name='Отображение',
                               choices=PAGE_TYPE_CHOICES)
    priority = models.IntegerField(default=0,
                                   verbose_name='Позиция')
    text = RichTextUploadingField(null=True,
                                  blank=True,
                                  verbose_name='Текст')
    keywords = models.TextField(null=True,
                                blank=True,
                                verbose_name='Ключевые слова')
    description = models.TextField(null=True,
                                   blank=True,
                                   verbose_name='Описание')

    translation_fields = ('title', 'text', 'keywords', 'description')
    i18n = TranslationField(fields=translation_fields)

    def __str__(self):
        return self.title_i18n

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def get_fields(self):
        return self.translation_fields


class ProductVideo(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Название')
    link = models.URLField(
        verbose_name='Ссылка',
        max_length=128,
        blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
