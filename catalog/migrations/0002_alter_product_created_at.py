# Generated by Django 5.0.3 on 2024-03-28 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateField(verbose_name='Дата создания (записи в БД)'),
        ),
    ]