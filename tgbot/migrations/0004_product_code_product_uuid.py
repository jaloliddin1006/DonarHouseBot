# Generated by Django 5.1.1 on 2025-01-08 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0003_alter_user_language_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.CharField(default=1, max_length=50, unique=True, verbose_name='Kod'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=1, editable=False, unique=True),
            preserve_default=False,
        ),
    ]