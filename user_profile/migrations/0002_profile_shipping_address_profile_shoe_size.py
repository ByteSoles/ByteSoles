# Generated by Django 5.1.2 on 2024-10-27 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='shipping_address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='shoe_size',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
