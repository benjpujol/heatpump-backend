# Generated by Django 4.1.7 on 2023-03-08 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heatloss', '0006_radiator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='radiator',
            old_name='radiator_depth',
            new_name='depth',
        ),
        migrations.RenameField(
            model_name='radiator',
            old_name='radiator_height',
            new_name='height',
        ),
        migrations.RenameField(
            model_name='radiator',
            old_name='radiator_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='radiator',
            old_name='radiator_width',
            new_name='width',
        ),
    ]
