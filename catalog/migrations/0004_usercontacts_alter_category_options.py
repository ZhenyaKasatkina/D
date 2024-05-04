# Generated by Django 5.0.3 on 2024-04-11 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_mycontact'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserContacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Адрес электронной почты')),
                ('message', models.TextField(blank=True, null=True, verbose_name='сообщение')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания (записи в БД)')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='Дата последнего изменения (записи в БД)')),
            ],
            options={
                'verbose_name': 'контакт',
                'verbose_name_plural': 'контакты',
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'категория', 'verbose_name_plural': 'категории'},
        ),
    ]