# Generated by Django 4.1.7 on 2023-02-28 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_building_renovationproject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='number_of_units',
        ),
    ]