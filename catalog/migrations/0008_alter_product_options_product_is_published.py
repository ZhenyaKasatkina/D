# Generated by Django 4.2.2 on 2024-05-07 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0007_product_owner"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "permissions": [
                    ("cancel_published_status", "Can unpublish product"),
                    ("can_edit_description", "Can edit product description"),
                    ("can_edit_category", "Can edit product category"),
                ],
                "verbose_name": "продукт",
                "verbose_name_plural": "продукты",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="is_published",
            field=models.BooleanField(default=False, verbose_name="Статус публикации"),
        ),
    ]
