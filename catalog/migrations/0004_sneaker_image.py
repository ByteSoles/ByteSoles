# Generated by Django 5.1.2 on 2024-10-24 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_category_alter_sneaker_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='sneaker',
            name='image',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
