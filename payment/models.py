from django.db import models

from payment.choices import PAYMENT_TYPE_CHOICES, PAYMENT_STATUS_CHOICES, PAYMENT_AGGREGATORS


class Payment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('order.Order',
                              on_delete=models.PROTECT,
                              verbose_name='Заказ')
    amount = models.FloatField(default=0,
                               verbose_name='Сумма заказа')
    deliver_price = models.BigIntegerField(default=0,
                                           verbose_name='Цена доставки')
    total = models.FloatField(default=0,
                              verbose_name='Итоговая сумма')
    state = models.IntegerField(default=0,
                                verbose_name='Статус')
    payment_type = models.CharField(max_length=100,
                                    choices=PAYMENT_TYPE_CHOICES,
                                    verbose_name='Тип оплаты')
    payment_aggregator = models.CharField(max_length=255,
                                          choices=PAYMENT_AGGREGATORS,
                                          verbose_name='Метод оплаты')
    transaction = models.ForeignKey('Transaction',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    verbose_name='Транзакция (click, payme)')

    def __str__(self):
        return str(self.order.pk)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплата'


class Transaction(models.Model):
    paycom_transaction_id = models.CharField(max_length=25)
    paycom_time = models.CharField(max_length=13)
    paycom_time_datetime = models.DateTimeField(auto_now_add=False)
    create_time = models.DateTimeField(auto_now_add=False)
    perform_time = models.DateTimeField(auto_now_add=False, null=True, default=None)
    cancel_time = models.DateTimeField(auto_now_add=False, null=True, default=None)
    amount = models.FloatField(default=0)
    state = models.IntegerField(default=0)
    reason = models.IntegerField(null=True, default=None)
    receivers = models.CharField(max_length=500, null=True, default=None)

    def __str__(self):
        return self.paycom_transaction_id
