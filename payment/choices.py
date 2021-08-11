PAYMENT_TYPE_CHOICES = (
    ('card', 'Карта'),
    ('cod', 'Оплата после доставки'),
    ('online', 'Онлайн'),
)

PAYMENT_STATUS_CHOICES = (
    ('payed', 'Оплачена'),
    ('wait', 'Ожидание оплаты'),
    ('canceled', 'Отменена'),
)

PAYMENT_AGGREGATORS = (
    ('apelsin', 'Апельсин (KapitalBank)'),
    ('payme', 'PayMe'),
    ('click', 'Click'),
    ('cash', 'Наличка'),
)
