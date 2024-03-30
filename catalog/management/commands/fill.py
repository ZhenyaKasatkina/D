import json
import os


from django.core.management import BaseCommand

from catalog.models import Product, Category
from config.settings import BASE_DIR

DIR = "fixtures"


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        """
        Получаем данные из фикстуры с категориями (JSON-файла)
        """
        with open(os.path.join(BASE_DIR, DIR, "catalog_data.json")) as json_file:
            data_list = json.load(json_file)
            # print(data_list)
            return data_list

    @staticmethod
    def json_read_products():
        """
        Получаем данные из фикстуры с продуктами (JSON-файла)
        """
        with open(os.path.join(BASE_DIR, DIR, "product_data.json")) as json_file:
            data_list = json.load(json_file)
            # print(data_list)
            return data_list

    def handle(self, *args, **options):
        Product.objects.all().delete()  # Удалите все продукты
        Category.objects.all().delete()  # Удалите все категории

        product_for_create = []  # Списки для хранения объектов
        category_for_create = []

        try:
            for category in Command.json_read_categories():
                category_for_create.append(Category(id=category["pk"],
                                                    category_name=category["fields"]["category_name"])
                                           )
            # Создаем объекты в базе с помощью метода bulk_create()
            Category.objects.bulk_create(category_for_create)
        except (ValueError, FileNotFoundError):
            pass

        try:
            for product in Command.json_read_products():
                product_for_create.append(Product(id=product["pk"],
                                                  product_name=product["fields"]["product_name"],
                                                  price=product["fields"]["price"],
                                                  category=product["fields"]["category"])
                                          )
                # Создаем объекты в базе с помощью метода bulk_create()
                Product.objects.bulk_create(product_for_create)

        except (ValueError, FileNotFoundError):
            pass
