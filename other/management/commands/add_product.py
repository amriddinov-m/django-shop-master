from django.core.management.base import BaseCommand
import psycopg2


from manufacturer.models import Manufacturer
from product.models import Product, ProductPhoto, NewCategory


class Command(BaseCommand):
    help = 'Add product'

    categories = {

    }

    def handle(self, *args, **options):
        try:
            mydb = psycopg2.connect(user="postgres",
                                    password="123",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="oldzender")
            mycursor = mydb.cursor()

            mycursor.execute("SELECT * FROM product_newcategory WHERE is_main=FALSE ")
            # mycursor.execute("SELECT * FROM oc_manufacturer")

            myresult = mycursor.fetchall()
            loop = 0
            for x in myresult:
                c = NewCategory()
                c.name = x[1]
                c.priority = x[2]
                c.icon = x[3]
                c.parent_id = x[8]
                c.is_main = False
                c.save()
        except (Exception, psycopg2.Error) as error:
            print(error)
        finally:
            # closing database connection.
            print("PostgreSQL connection is closed")
