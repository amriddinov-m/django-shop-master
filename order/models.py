from django.db import models
from modeltrans.fields import TranslationField

from order.choices import ORDER_STATUS_CHOICES
from bot.tasks import send_order
from payment.choices import PAYMENT_TYPE_CHOICES


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('user.User',
                             on_delete=models.PROTECT,
                             verbose_name='Пользователь',
                             null=True,
                             blank=True)
    guest = models.ForeignKey('GuestAddress',
                              on_delete=models.PROTECT,
                              null=True,
                              blank=True)
    user_address = models.ForeignKey('user.UserAddress',
                                     on_delete=models.PROTECT,
                                     null=True,
                                     blank=True)
    status = models.CharField(max_length=40,
                              choices=ORDER_STATUS_CHOICES,
                              default='created',
                              verbose_name='Статус заказа')
    is_paid = models.BooleanField(default=False,
                                  verbose_name='Оплачено')
    products = models.ManyToManyField('OrderItem',
                                      null=True,
                                      blank=True,
                                      verbose_name='Товары')
    comments = models.TextField(null=True,
                                blank=True,
                                verbose_name='Комментарии')
    last_changed_date = models.DateTimeField(auto_now=True)
    deliver = models.ForeignKey('Deliver',
                                on_delete=models.PROTECT,
                                verbose_name='Метод доставки',
                                null=True,
                                blank=True)
    payment_method = models.CharField(max_length=255,
                                      verbose_name='Метод оплаты',
                                      choices=PAYMENT_TYPE_CHOICES)
    total = models.BigIntegerField(default=0,
                                   verbose_name='Итоговая сумма')
    products_init = models.BooleanField(default=False)
    send_admin = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Order, self).save()
        if not self.send_admin and self.products_init:
            if self.is_paid:
                payment_status = 'Оплачено'
            else:
                payment_status = 'Не Оплачено'
            text = generate_admin_invoice_text(self.products.all(), payment_status, self.user.phone, self.comments,
                                               dict(PAYMENT_TYPE_CHOICES)[self.payment_method], self.pk)
            send_order.delay(text)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказ'


class GuestAddress(models.Model):
    fullname = models.CharField(max_length=255,
                                verbose_name='ФИО')
    email = models.CharField(max_length=255,
                             verbose_name='Почта',
                             null=True,
                             blank=True)
    phone = models.CharField(max_length=255,
                             verbose_name='Номер телефона',
                             null=True,
                             blank=True)
    address = models.CharField(max_length=255,
                               verbose_name='Адрес')

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Контакты гостей'
        verbose_name_plural = 'Контакты гостей'


class OrderItem(models.Model):
    product = models.ForeignKey('product.Product',
                                on_delete=models.PROTECT,
                                verbose_name='Товар')
    count = models.IntegerField(default=0,
                                verbose_name='Количество')
    price = models.BigIntegerField(default=0,
                                   verbose_name='Цена')

    def __str__(self):
        return self.product.title_i18n

    class Meta:
        verbose_name = 'Товары заказа'
        verbose_name_plural = 'Товары заказа'


class Deliver(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Название')
    price = models.FloatField(default=0,
                              verbose_name='Цена')
    translation_fields = ('title',)
    i18n = TranslationField(fields=translation_fields)

    def __str__(self):
        return self.title_i18n

    def get_fields(self):
        return self.translation_fields

    class Meta:
        verbose_name = 'Метод доставки'
        verbose_name_plural = 'Метод доставки'


class ProductCall(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    number = models.CharField(max_length=255,
                              verbose_name='Номер клиента')
    name = models.CharField(max_length=255,
                            verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Звонок'
        verbose_name_plural = 'Звонки'


class ProductMailing(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=255,
                             verbose_name='Почта')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


# Bot order message generate
def generate_admin_basket_text(products):
    _text = ''
    _count = 1
    total_price = 0
    _text = '🛒Список продуктов:\n'
    print(products)
    for prod in products:
        print(prod)
        _text += str(_count) + '. <b>' + prod.product.title + ' (' + prod.product.article+')' \
                 + '</b>' + ' x ' + str(prod.count) + '\n'
        _count += 1
        total_price += prod.product.price * prod.count
        _text += 'Итого: <b>' + str(total_price) + '</b>\n'
    return _text


def generate_admin_invoice_text(products, is_paid, phone, comment, payment_method, pk):
    _text = generate_admin_basket_text(products)
    _text += '\n----------------------\n'
    _text += '\n📞Номер телефона: ' + str(phone)
    _text += '\n📝Комментарий: ' + str(comment)
    _text += '\n💰Тип оплаты: ' + str(payment_method)
    _text += '\nНомер заказа: ' + str(pk)
    _text += '\nСтатус оплаты: ' + str(is_paid)
    return _text

