from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")

    avatar = models.ImageField(
        upload_to="users/avatar/", verbose_name="аватар", **NULLABLE
    )
    phone = models.CharField(max_length=20, verbose_name="телефон", **NULLABLE)
    country = models.CharField(max_length=50, verbose_name="страна", **NULLABLE)
    token = models.CharField(max_length=100, verbose_name="token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"  # Настройка для наименования одного объекта
        verbose_name_plural = (
            "пользователи"  # Настройка для наименования набора объектов
        )
