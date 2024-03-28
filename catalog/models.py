from datetime import date

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    category_name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.category_name} ({self.description})'

    class Meta:
        verbose_name = 'Категория'            # Настройка для наименования одного объекта
        verbose_name_plural = 'Категории'    # Настройка для наименования набора объектов


class Product(models.Model):
    product_name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='preview/', verbose_name='превью', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateField(auto_now_add=False,           # default=date.today,
                                  verbose_name='Дата создания (записи в БД)')
    updated_at = models.DateField(auto_now=False, verbose_name='Дата последнего изменения (записи в БД)')
    manufactured_at = models.DateField(verbose_name='Дата производства продукта', **NULLABLE)

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.product_name}, цена: {self.price} ({self.description})'

    class Meta:
        verbose_name = 'продукт'            # Настройка для наименования одного объекта
        verbose_name_plural = 'продукты'    # Настройка для наименования набора объектов
