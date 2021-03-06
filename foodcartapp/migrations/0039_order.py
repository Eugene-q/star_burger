# Generated by Django 3.2 on 2022-04-15 22:56

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_alter_product_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50, verbose_name='имя')),
                ('lastname', models.CharField(blank=True, max_length=50, verbose_name='фамилия')),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='телефон')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='адрес доставки')),
            ],
        ),
    ]
