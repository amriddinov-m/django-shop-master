import os

from django.core.management.base import BaseCommand
import sqlite3

from dsshop.settings import BASE_DIR
from manufacturer.models import Manufacturer
from product.models import Product, NewCategory


class Command(BaseCommand):
    help = 'Add product'

    def handle(self, *args, **options):
        try:
            sqliteConnection = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
            cursor = sqliteConnection.cursor()
            print("Database created and Successfully Connected to SQLite")

            sqlite_select_Query = "select * from manufacturer_manufacturer "
            cursor.execute(sqlite_select_Query)
            record = cursor.fetchall()

            print(record[0])
            for r in record:
                cat = Manufacturer()
                cat.name = r[1]
                cat.icon = r[2]
                # cat.save()
            cursor.close()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
