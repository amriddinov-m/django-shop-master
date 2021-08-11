DELIVER_TYPE_CHOICES = (
    ('created', 'Заказ Создан'),
    ('available', 'Есть в наличии'),
)

DISCOUNT_TYPE_CHOICES = (
    ('none', 'Без скидки'),
    ('percent', 'Процент'),
    ('amount', 'Сумма')
)
SERVICES_TYPE_CHOICES = (
    ('Installation', 'Монтаж'),
    ('deliver', 'Доставка')
)

STATUS_TYPE_CHOICES = (
    ('Yes', 'Да'),
    ('No', 'Нет')
)
CURRENCY_TYPE_CHOICES = (
    ('RUB', 'RUB'),
    ('USD', 'USD'),
    ('USD1', 'USD1'),
    ('USD2', 'USD2'),
    ('USD3', 'USD3'),
    ('EUR', 'EUR'),
    ('EUR1', 'EUR1'),
    ('EUR2', 'EUR2'),
    ('EUR3', 'EUR3'),
)
LANGUAGE_TYPE_CHOICES = (
    ('Ru', 'Ru'),
    ('En', 'En')
)
TOP_TYPE_CHOICES = (
    ('Top', 'Топ'),
    ('Usual', 'Обычный')
)
PAGE_TYPE_CHOICES = (
    ('Nowhere', 'Нигде'),
    ('menu', 'В меню'),
    ('basement', 'В подвале'),
    ('menu and basement', 'В меню и подвале')
)
PARENT_TYPE_CHOICES = (
    ('Parent page', 'Выберите родительскую страницу'),
    ('Us', 'О нас'),
)
