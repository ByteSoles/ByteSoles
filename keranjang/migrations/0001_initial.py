# Generated by Django 5.1.2 on 2024-11-22 11:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sneaker_name', models.CharField(max_length=255)),
                ('sneaker_price', models.IntegerField(default=0)),
                ('sneaker_image', models.URLField()),
                ('quantity', models.IntegerField(default=0)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.IntegerField(default=0)),
                ('sneaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.sneaker')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_items', models.IntegerField(default=0)),
                ('total_price', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
