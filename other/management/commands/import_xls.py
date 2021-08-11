import os
from datetime import datetime

import pandas as pd

from django.core.management.base import BaseCommand

from dsshop.settings import BASE_DIR
from product.models import Product


class Command(BaseCommand):
    help = 'Add product'

    categories = {

    }

    def handle(self, *args, **options):
        file = os.path.join(BASE_DIR, 'products.xlsx')
        df = pd.read_excel(file)
        for i in df.index:
            try:
                price = self.to_digit(df['price'][i])
                product = Product.objects.get(article=df['article'][i])
                if float(product.price) != float(price):
                    product.price = price
                    product.last_price_update = datetime.now()
                    product.save()
            except Product.DoesNotExist:
                price = self.to_digit(df['price'][i])
                product = Product()
                product.article = df['article'][i]
                product.title = df['title'][i]
                product.price = price
                product.save()

    def to_digit(self, val):
        try:
            res = float(val.replace(' у.е.', '').replace(',', '.').replace('\xa0', ''))
        except ValueError:
            print(val)
            res = 0
        return res
