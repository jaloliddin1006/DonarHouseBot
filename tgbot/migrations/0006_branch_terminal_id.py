# Generated by Django 5.1.1 on 2025-01-09 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0005_order_iiko_order_id_order_latitude_order_longitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='terminal_id',
            field=models.UUIDField(default='90cf7ac5-7d2c-070a-0189-637b206e0064'),
            preserve_default=False,
        ),
    ]