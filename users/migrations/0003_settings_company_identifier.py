# Generated by Django 4.1.7 on 2023-03-08 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='company_identifier',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
