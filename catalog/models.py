from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class MyContact(models.Model):
    """Контакты владельца сайта"""

    contact_name = models.CharField(max_length=150, verbose_name="Наименование")
    country = models.CharField(max_length=100, verbose_name="Страна")
    inn = models.PositiveBigIntegerField(verbose_name="ИНН")
    address = models.TextField(verbose_name="Почтовый адрес", **NULLABLE)
    email = models.EmailField(verbose_name="Адрес электронной почты")
    logo = models.ImageField(
        upload_to="preview/", verbose_name="Логотип сайта", **NULLABLE
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name="Дата создания (записи в БД)"
    )
    updated_at = models.DateField(
        auto_now=True, verbose_name="Дата последнего изменения (записи в БД)"
    )

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.contact_name}, ИНН: {self.inn} ({self.country}, {self.country}, {self.email})"

    class Meta:
        verbose_name = "контакт"  # Настройка для наименования одного объекта
        verbose_name_plural = "контакты"  # Настройка для наименования набора объектов


class UserContacts(models.Model):
    """Контакты, сообщение, поступившие от пользователя"""

    name = models.CharField(max_length=150, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Адрес электронной почты")
    message = models.TextField(verbose_name="сообщение", **NULLABLE)
    created_at = models.DateField(
        auto_now_add=True, verbose_name="Дата создания (записи в БД)"
    )
    updated_at = models.DateField(
        auto_now=True, verbose_name="Дата последнего изменения (записи в БД)"
    )

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.name} ({self.phone}, {self.email}): {self.message}"

    class Meta:
        verbose_name = "контакт"  # Настройка для наименования одного объекта
        verbose_name_plural = "контакты"  # Настройка для наименования набора объектов


class Category(models.Model):
    """Категории"""

    category_name = models.CharField(max_length=150, verbose_name="наименование")
    description = models.TextField(verbose_name="описание", **NULLABLE)

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.category_name} ({self.description})"

    class Meta:
        verbose_name = "категория"  # Настройка для наименования одного объекта
        verbose_name_plural = "категории"  # Настройка для наименования набора объектов


class Product(models.Model):
    """Продукты"""

    product_name = models.CharField(max_length=150, verbose_name="наименование")
    description = models.TextField(verbose_name="описание", **NULLABLE)
    preview = models.ImageField(upload_to="preview/", verbose_name="превью", **NULLABLE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="категория"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за покупку"
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name="Дата создания (записи в БД)"
    )
    updated_at = models.DateField(
        auto_now=True, verbose_name="Дата последнего изменения (записи в БД)"
    )
    # manufactured_at = models.DateField(verbose_name='Дата производства продукта', **NULLABLE)
    owner = models.ForeignKey(
        User,
        verbose_name="владелец",
        on_delete=models.SET_NULL,
        **NULLABLE,
        help_text="чья вкусняшка?",
    )

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.product_name}, цена: {self.price} ({self.description})"

    class Meta:
        verbose_name = "продукт"  # Настройка для наименования одного объекта
        verbose_name_plural = "продукты"  # Настройка для наименования набора объектов


class Version(models.Model):
    """Версия"""

    product = models.ForeignKey(
        Product,
        related_name="version",
        on_delete=models.CASCADE,
        verbose_name="продукт",
        **NULLABLE,
    )
    version_number = models.CharField(
        max_length=5, default="Aa001", verbose_name="номер версии"
    )
    version_name = models.CharField(max_length=150, verbose_name="название версии")
    is_active = models.BooleanField(default=True, verbose_name="активная версия")

    def __str__(self):
        # Строковое отображение объекта
        return f"версия: {self.version_number} ({self.version_name})"

    class Meta:
        verbose_name = "версия"  # Настройка для наименования одного объекта
        verbose_name_plural = "версии"  # Настройка для наименования набора объектов


class Blog(models.Model):
    """Блог"""

    title = models.CharField(max_length=150, verbose_name="заголовок")
    slug = models.CharField(max_length=150, verbose_name="slug", **NULLABLE)
    content = models.TextField(verbose_name="содержимое", **NULLABLE)
    preview = models.ImageField(upload_to="preview/", verbose_name="превью", **NULLABLE)
    created_at = models.DateField(
        auto_now_add=True, verbose_name="Дата создания (записи в БД)"
    )
    is_published = models.BooleanField(default=True, verbose_name="опубликовано")
    views_count = models.IntegerField(default=0, verbose_name="просмотры")

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.title} ({self.views_count}, {self.slug}): {self.content}."

    class Meta:
        verbose_name = "блог"  # Настройка для наименования одного объекта
        verbose_name_plural = "блоги"  # Настройка для наименования набора объектов
