# Generated by Django 5.1.2 on 2024-10-22 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sneaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_sneakers', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('release_date', models.DateField()),
            ],
        ),
    ]
