# Generated by Django 4.1.7 on 2023-03-11 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heatloss', '0013_remove_wall_wall_height_wall_number_of_storeys_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wall',
            name='wall_area',
            field=models.FloatField(),
        ),
    ]