# Generated by Django 4.1.7 on 2023-03-01 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_customer_eligible_for_subsidy_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='hot_water_system',
            field=models.CharField(default='boiler', max_length=50),
            preserve_default=False,
        ),
    ]