# Generated by Django 4.1.7 on 2023-03-08 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_building_occupancy_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='user',
            new_name='customuser',
        ),
    ]
